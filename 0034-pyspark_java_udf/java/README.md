# Compile
Single file:

	javac -cp "jars/h3.jar;jars/spark-sql.jar" SimpleH3.java

Folder:

	javac -cp "jars/h3.jar;jars/spark-sql.jar" com\villoro\simpleH3\*.java

# Jar
Single file

	jar cvf SimpleH3.jar SimpleH3.class

Folder

	jar cvf SimpleH3.jar com\villoro\simpleH3\*.class

# Links
https://www.baeldung.com/java-create-jar


