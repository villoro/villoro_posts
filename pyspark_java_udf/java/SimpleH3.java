import java.io.IOException;
import com.uber.h3core.H3Core;

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