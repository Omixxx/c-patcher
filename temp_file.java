//		public static void main(String[] args) throws Exception{
//		    if (args.length != 1) {
//		        throw new RuntimeException("Need 1 parameter: the JavaParser source checkout root directory.");
//		    }
//		    Log.setAdapter(new Log.StandardOutStandardErrorAdapter());
//		    final Path root = Paths.get(args[0], "..", "javaparser-core", "src", "main", "java");
//		    final SourceRoot sourceRoot = new SourceRoot(root, parserConfiguration);
//		    StaticJavaParser.setConfiguration(parserConfiguration);
//		    final Path generatedJavaCcRoot = Paths.get(args[0], "..", "javaparser-core", "target", "generated-sources", "javacc");
//		    final SourceRoot generatedJavaCcSourceRoot = new SourceRoot(generatedJavaCcRoot, parserConfiguration);
//		    new CoreGenerator().run(sourceRoot, generatedJavaCcSourceRoot);
//		    sourceRoot.saveAll();
//		}
 public static void main 