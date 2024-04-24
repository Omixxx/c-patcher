class DummyClass{
	 public   static   hashBasedTable < r,   c,   v >   create ( inT   expectedRows,   inT   expectedCellsPerRow ) { 
       checkNonNegative ( expectedCellsPerRow,   $string$ ) ; 
       map < r,   map < c,   v >>   backingMap   =   maps. newLinkedHashMapWithExpectedSize ( expectedRows ) ; 
       return   new   hashBasedTable < > ( backingMap,   new   factory < c,   v > ( expectedCellsPerRow ) ) ; 
 	 }

}