The main content in each file:

Java.pdf
-Java platform: JRE and JDK
-CLASSPATH set
-naming rule (package, class, variable, fuction, constant)
-strong-typed
-data type: class, interface
	    short,int,long,char,boolean
- &  <<  >>  |
-ternary conditional (...)?...:...
- if; switch; while
-method 
 overload (same method name,different parameters,has no relationship with return value)
-stack,heap, method,static ,register ???
 garbage collection
-Array
 ArrayIndexOutOfBoundsException
 NullPointerException
-object-oriented concept
 class   object
 encapsulation
 inheritance
 polymorphism (override)
-anonymous object
-Constructor (constructor methods overload)
-this
-static


Java2.pdf
-the reletionship between classes: is a
-super
-inheritance: override
-final
-inner class?
-abstract (class/method)
-interface attributes: public static final
           method : public abstract
-class not support multi-inheritance
 interface supprt multi-implement
-polymorphism for attributes, compile time , run time depends on the left side (reference)
              for methods, compile time (reference) runtime (object)
-嵌套类？内部匿名类？？
-Throwable (inheritances from java.lang.object)	
    |-error
    |-exception
-try catch finally
-Exception e
 System.out.println(e.toString())
 System.out.println(e.getMessage())
 e.printStackTrace()
-throw + Exception object
 throws?? + Exception class
-multi exceptions
-self-defined exception extends Exception extends Throwable
-RuntimeException 
-the exception relationship between the father class and the inhertance class (derived class)
-package???

Java3,pdf
-process thread
-exteands Thread  override run ()
-static Thread currentThread()
 getName()
-implements Runnable
 new Thread (new ... ()).start()
 advantage : avoids single inheritanced
-synchronized (object)
 {
   synchronized code
  }

Java4.pdf
- Java.lang.Object  wait(),  notify(), notifyAll()  
-use while
-use notifyAll
-condition: await(),  signal(),   signalAll()???
-interrupt() to stop the thread?
-t1.setDaemon(true)
-  .join()

Java5.pdf
-String constant pool
-String: s1.equals(s2)   contains(str) 
         char[] toCharArray()            String(char[])  
         String(byte[],offset,count)     byte[] getBytes()
         replace       split       substring
         trim          compareTo
-StringBuffer (conatiner):  --- toSting -String
         C create U update R read D delete
         append()    insert()
-StringBuilder (not synchronized, used in one thread)
-Integer.parseInt()       Double.parseDouble()
-Integer  Boolean

Java6.pdf
-java.util.Collection
-Iterator (inner class)
-List 
     ArrayList: quick for searching
     LinkedList: quick for delete or add
     Vector
-List (feature: index)
-Set ---HashSet hashCode;equals
     ---TreeSet compareTo
-interface Comparator  override compare method
-generics         
-？extends E
 ？super E
-Map (key-value)
    |-HashMap
    |-TreeMap
-Set<k> keySet()
 Set<Map.Entry<k,v>> entrySet()    data type:Map.Entry
-Map:interface 
 Entry:the interface inside Map
-Collections
-Arrays
-advanced for (instead of interator)

Java7.pdf
-System?
-Properties prop = System.getProperties()
-Runtime r = Runtime.getRuntime()
-Calendar c = Calendar.getInstance()
-InputStream OutputStream
-Reader Writer
-File
-recursion
-PrintWriter PrintStream
-ObjectInpuStream ObjectOutputStream
 the class should implements Serializable
 Serializable UID







   






        
 

