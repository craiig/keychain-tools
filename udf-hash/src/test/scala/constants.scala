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
    itShouldValueHash("valuehash-ints", 1, 1)
    itShouldValueHash("valuehash-arrays", Array(1,2,3), Array(1,2,3))
    itShouldValueHash("valuehash-tuples", (1,2,3), (1,2,3))

    case class TestObject(one: String, two: Int, three: Long);
    itShouldValueHash("valuehash-caseclass", TestObject("1",2,3), TestObject("1",2,3))

    case class NestedObject(one: TestObject, two: Array[Int], three: Long)
    val a = Array(1,2,3)
    val b = Array(1,2,3)
    val to1 = TestObject("1", 2, 3)
    val to2 = TestObject("1", 2, 3)
    itShouldValueHash("valuehash-nested", NestedObject(to1, a, 666), NestedObject(to2, b, 666))

  }
}
