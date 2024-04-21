class DummyClass{
	 private   void   annotate ( T   node,   Class <? >   annotation,   Expression   content ) { 
       node. setAnnotations ( node. getAnnotations ( ). stream ( ). filter ( a   - >  ! a. getNameAsString ( ). equals ( annotation. getSimpleName ( ) ) ). collect ( toNodeList ( ) ) ) ; 
       node. addSingleMemberAnnotation ( annotation. getSimpleName ( ),   a. getMessage ( ) ) ; 
       node. tryAddImportToParentCompilationUnit ( annotation ) ; 
 	 }

}