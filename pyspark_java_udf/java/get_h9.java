import java.io.IOException;
import com.uber.h3core.H3Core;
import org.apache.spark.sql.api.java.UDF2;

public class get_h9 implements UDF2<Double, Double, String> {

    @Override
    public String call(Double longitude, Double latitude) throws Exception {
        try {
            H3Core h3 = H3Core.newInstance();
            return h3.geoToH3Address(longitude, latitude, 9);
        }
        catch(IOException e) {
            return null;
        }
    }
}