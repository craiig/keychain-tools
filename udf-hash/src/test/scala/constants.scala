package ca.ubc.ece.systems

import ca.ubc.ece.systems.ClosureHashFunSpec

class Constants extends ClosureHashFunSpec {
  describe("constants"){
    itShouldHash(
      "fold-right"
      , (x:Int) => {x+2}
      , (x:Int) => {x+1+1}
    )
    itShouldHash("fold-right-assoc"
      , (x:Int) => {x+2}
      , (x:Int) => {x+(1+1)}
    )
    itShouldHash("fold-left"
      , (x:Int) => {2+x}
      , (x:Int) => {1+1+x}
    )
    itShouldHash("fold-left-assoc"
      , (x:Int) => {2+x}
      , (x:Int) => {(1+1)+x}
    )
    itShouldHash("canonicalize-left-right"
      , (x:Int) => {2+x}
      , (x:Int) => {x+2}
    )
    itShouldHashNoTrace("notrace-fold-right"
      , (x:Int) => {x+2}
      , (x:Int) => {x+1+1}
    )
    itShouldHashNoTrace("notrace-fold-right-assoc"
      , (x:Int) => {x+2}
      , (x:Int) => {x+(1+1)}
    )
    itShouldHashNoTrace("notrace-fold-left"
      , (x:Int) => {2+x}
      , (x:Int) => {1+1+x}
    )
    itShouldHashNoTrace("notrace-fold-left-assoc"
      , (x:Int) => {2+x}
      , (x:Int) => {(1+1)+x}
    )
    itShouldHashNoTrace("notrace-canonicalize-left-right"
      , (x:Int) => {2+x}
      , (x:Int) => {x+2}
    )
  }
}
