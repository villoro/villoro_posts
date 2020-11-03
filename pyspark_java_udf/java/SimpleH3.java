import java.io.IOException;
import com.uber.h3core.H3Core;
import org.apache.spark.sql.api.java.UDF2;

class SimpleH3
{ 
    public static String get_h8(int longitude, int latitude){
        try {
            H3Core h3 = H3Core.newInstance();
            return h3.geoToH3Address(longitude, latitude, 8);
        }
        catch(IOException e) {
            return null;
        }
    }
} 

public class get_h9 implements UDF2<Float, Float, String> {

    static H3Core h3 = H3Core.newInstance();

    @Override
    public String call(Float longitude, Float latitude) throws Exception {
        return h3.geoToH3Address(longitude, latitude, 9);
    }
}