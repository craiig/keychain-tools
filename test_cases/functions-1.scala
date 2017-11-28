sc.hash((x:Int) => {x})

vs

 def test(x:Int): Int = { x }
 sc.hash(test(_))


 //issue seems to be that scala does not detect these two functions as equivalent because their types are different
 //scala> (x:Int) => {x}
 //res27: Int => Int = <function1>
 //
 //scala> def test(x:Int): Int = {  x }
 //test: (x: Int)Int
 //interesting because signature of test(_) and (x:Int) => {x} is the same
 //scala> test(_)
 //res28: Int => Int = <function1>
