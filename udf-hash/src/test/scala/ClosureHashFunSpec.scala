package ca.ubc.ece.systems
import org.scalatest.fixture.FunSpec
import org.scalatest.fixture.TestDataFixture
import org.scalatest.TestData
import ca.ubc.ece.systems.{ClosureHash => ch}
import scala.collection.mutable.HashMap

//for JSON logging
import org.json4s._
import org.json4s.jackson.Serialization
import org.json4s.jackson.Serialization.{write => WriteJson}
import java.io.{File,FileWriter}

abstract class ClosureHashFunSpec extends FunSpec with TestDataFixture {
  implicit val jsonformats = Serialization.formats(NoTypeHints)

  def itShouldHash(name:String, left:AnyRef, right:AnyRef) = {
    it(name){ td =>
      val left_hashWithTrace = ch.hashWithTrace(left, true)
      assert(!left_hashWithTrace.isEmpty)
      val right_hashWithTrace = ch.hashWithTrace(right, true)
      assert(!right_hashWithTrace.isEmpty)

      val left_hash = left_hashWithTrace.get._1
      val left_hash_trace = left_hashWithTrace.get._2
      val right_hash = right_hashWithTrace.get._1
      val right_hash_trace = right_hashWithTrace.get._2

      // Log the hash trace of each test
      //if(left_hash != right_hash){
        var filename = s"${td.scopes.mkString("-")}-${td.text}"
        var parent_dir = "target/hash_traces/"
        (new File(parent_dir)).mkdirs()
        var left_file = s"${parent_dir}/${filename}_left.json"
        var right_file = s"${parent_dir}/${filename}_right.json"
        
        def writeFile(name:String, str:String) = {
          val fw = new FileWriter(name)
          fw.write(str)
          fw.close
        }
        writeFile(left_file, WriteJson(left_hash_trace))
        writeFile(right_file, WriteJson(right_hash_trace))
      //}

      /* don't fail any tests, we check that hashes match in the resilience benchmark */
      //assert(left_hash == right_hash)
    }
  }
  def itShouldHashNoTrace(name:String, left:AnyRef, right:AnyRef) = {
    it(name){ td =>
      val left_hashWithTrace = ch.hashWithTrace(left, false)
      assert(!left_hashWithTrace.isEmpty)
      val right_hashWithTrace = ch.hashWithTrace(right, false)
      assert(!right_hashWithTrace.isEmpty)

      val left_hash = left_hashWithTrace.get._1
      val left_hash_trace = left_hashWithTrace.get._2
      val right_hash = right_hashWithTrace.get._1
      val right_hash_trace = right_hashWithTrace.get._2

      assert(left_hash_trace("primitives").asInstanceOf[HashMap[String,Any]]("trace") == "")
      assert(left_hash_trace("bytecode").asInstanceOf[HashMap[String,Any]]("trace") == "")
      assert(right_hash_trace("primitives").asInstanceOf[HashMap[String,Any]]("trace") == "")
      assert(right_hash_trace("bytecode").asInstanceOf[HashMap[String,Any]]("trace") == "")

      /* don't fail any tests, we check that hashes match in the resilience benchmark */
      //assert(left_hash == right_hash)
    }
  }
}
