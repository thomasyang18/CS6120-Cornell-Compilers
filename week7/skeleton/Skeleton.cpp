#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/IR/Constant.h"
#include "llvm/IR/InstrTypes.h"
#include "llvm/IR/IRBuilder.h"



using namespace llvm;

// The goal of this skeleton is to change any constants that are generated
// in the LLVM to random integers between 1 and 100
// 

namespace {
  struct SkeletonPass : public FunctionPass {
    static char ID;
    SkeletonPass() : FunctionPass(ID) {}

    virtual bool runOnFunction(Function &F) {
		bool modified = false;
      for (auto I = inst_begin(F), E = inst_end(F); I != E; ++I){ 
	//for (auto &B: F) for (auto &I : B){
	    if (auto *op = dyn_cast<StoreInst>(&*I)){
	  	
		IRBuilder<> builder(op);
		Value *lhs = op->getOperand(0);
		Value *rhs = op->getOperand(1);
	
		if (isa<ConstantInt>(lhs)){
		 	errs() << "Lhs was a constant Int!" << '\n';
		}
		else continue;
		Value *newLHS = ConstantInt::get(Type::getInt64Ty(F.getContext()), rand());

		Value *newOp = builder.CreateStore(newLHS, rhs);

		for (auto &U : op->uses()){
			User *user = U.getUser();
			user->setOperand(U.getOperandNo(), newOp);
		}
		
		modified = true;
		
	  }
	  
      }
    
      return modified;
    }
  };
}

char SkeletonPass::ID = 0;

// Automatically enable the pass.
// http://adriansampson.net/blog/clangpass.html
static void registerSkeletonPass(const PassManagerBuilder &,
                         legacy::PassManagerBase &PM) {
  PM.add(new SkeletonPass());
}
static RegisterStandardPasses
  RegisterMyPass(PassManagerBuilder::EP_EarlyAsPossible,
                 registerSkeletonPass);
