/*BEGIN_LEGAL 
Intel Open Source License 

Copyright (c) 2002-2014 Intel Corporation. All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.  Redistributions
in binary form must reproduce the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.  Neither the name of
the Intel Corporation nor the names of its contributors may be used to
endorse or promote products derived from this software without
specific prior written permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE INTEL OR
ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
END_LEGAL */
#include <signal.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <set>
#include "pin.H"

UINT64 icount = 0;

#include "swizzle_util.h"

// When an image is loaded, check for a MyAlloc function
VOID Image(IMG img, VOID *v)
{
    //fprintf(stderr, "Loading %s\n",IMG_name(img));
    
    for (SEC sec = IMG_SecHead(img); SEC_Valid(sec); sec = SEC_Next(sec))
    {
        //fprintf(stderr, "  sec %s\n", SEC_name(sec).c_str());
        for (RTN rtn = SEC_RtnHead(sec); RTN_Valid(rtn); rtn = RTN_Next(rtn))
        {
            //fprintf(stderr, "    rtn %s\n", RTN_name(rtn).c_str());
            // Swizzle the return value of MyAlloc
            
            if (RTN_Name(rtn) == "MyAlloc")
            {
                RTN_Open(rtn);
                
                fprintf(stderr, "Adding Swizzle to %s\n", "MyAlloc");
                RTN_InsertCall(rtn, IPOINT_AFTER, AFUNPTR(SwizzleRef), IARG_FUNCRET_EXITPOINT_REFERENCE, IARG_END);
                RTN_Close(rtn);
            }

            if (RTN_Name(rtn) == "MyFree")
            {
                RTN_Open(rtn);

                fprintf(stderr, "Adding SwizzleArg to %s\n", "MyFree");
                RTN_InsertCall(rtn, IPOINT_BEFORE, AFUNPTR(UnswizzleRef), IARG_FUNCARG_ENTRYPOINT_REFERENCE, 0, IARG_END);
                RTN_Close(rtn);
            }
        }
    }
}

VOID RewriteIns(INS ins)
{
    //fprintf(stderr,"Rewriting %p\n",(void*)INS_Address(ins));
    
    for (UINT32 memopIdx=0; memopIdx < INS_MemoryOperandCount(ins); memopIdx++)
    {
        REG scratchReg = REG(int(REG_INST_G0)+memopIdx);

        INS_InsertCall(ins, IPOINT_BEFORE,
                       AFUNPTR(Unswizzle),
                       IARG_MEMORYOP_EA, memopIdx,
                       IARG_RETURN_REGS, scratchReg, IARG_END);
        INS_RewriteMemoryOperand(ins, memopIdx, scratchReg); 
    }
}

set<ADDRINT> SwizzleRefs;

BOOL SegvHandler(THREADID, INT32, CONTEXT *ctxt, BOOL, const EXCEPTION_INFO *, void *)
{
    ADDRINT address = PIN_GetContextReg(ctxt, REG_INST_PTR);

    //fprintf(stderr, "Fault at %p\n",(void*)address);
    
    if (SwizzleRefs.find(address) != SwizzleRefs.end())
    {
        return true;
    }
    
    // The next time we see this address, it requires swizzling
    SwizzleRefs.insert(address);
    
    // Invalidate this instruction in code cache so it will be reinstrumented
    CODECACHE_InvalidateRange(address, address + 20);

    // returning from the signal handler will re-execute the instruction
    // this time it will be swizzled
    return false;
}

    
VOID Trace(TRACE trace, VOID *v)
{
    BOOL rewrite = false;
    
    for (BBL bbl = TRACE_BblHead(trace); BBL_Valid(bbl); bbl = BBL_Next(bbl))
    {
        for (INS ins = BBL_InsHead(bbl); INS_Valid(ins); ins = INS_Next(ins))
        {
            // If we see an instruction that needs rewriting, then rewrite all
            if (SwizzleRefs.find(INS_Address(ins)) != SwizzleRefs.end())
                rewrite = true;
        
            if (rewrite)
            {
                // If we suspect this instruction needs to be swizzled, generate safe, but slow code
                RewriteIns(ins);
            }
        }
    }
}

int main(int argc, char * argv[])
{
    PIN_InitSymbols();
    PIN_Init(argc, argv);

    TRACE_AddInstrumentFunction(Trace, 0);
    IMG_AddInstrumentFunction(Image, 0);
    
    if (!PIN_InterceptSignal(SIGSEGV, SegvHandler, 0))
	{
		fprintf (stderr, "InterceptSignal failed\n");
		exit (1);
	}

    // Never returns
    PIN_StartProgram();
    
    return 0;
}
