package org.apache.spark.HashTesting

import org.apache.spark.util.ClosureCleaner

object Constants1 {
  def main(args: Array[String]): Unit = {
    val cc = ClosureCleaner
    val leftfunc = (x:Int) => x+1
    val rightfunc = (x:Int) => x+1
    val left = cc.hashWithTrace(leftfunc)
    val right = cc.hashWithTrace(rightfunc)
    //val left = cc.hashWithTrace((x:Int) => x+10)
    //val right = cc.hashWithTrace((x:Int) => x+1)
  }
}
