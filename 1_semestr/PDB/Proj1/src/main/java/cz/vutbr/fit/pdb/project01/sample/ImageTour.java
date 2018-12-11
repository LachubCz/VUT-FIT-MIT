package multimedia;

import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import oracle.ord.im.OrdImage;
import oracle.jdbc.OraclePreparedStatement;
import java.sql.PreparedStatement;
import java.util.ArrayList;
import java.util.List;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.embed.swing.SwingFXUtils;
import javafx.scene.image.Image;
import javax.imageio.ImageIO;
import oracle.jdbc.OracleResultSet;

/**
 * Class which allows manipulation with tour picture saved in the remote database
 * @author Richard Hauerland
 */
public class ImageTour
{
    /**
     * Variable which holds connection to the database
     */
    private Connection connection;

    /**
     * Pass connection variable into the class instance
     * @param Connection variable
     * @return Returns instance of the same object
     * @throws SQLException
     */
    public ImageTour(Connection _connection) throws SQLException {
        this.connection = _connection;
    }

    /**
     * Method which returns proxy of image saved in remote database
     * @param Integer index of desired image
     * @return OrdImage variable which represents JDBC image
     * @throws SQLException
     */
    public OrdImage getProxy(int id) throws SQLException
    {
        OrdImage imgProxy = null;
        OraclePreparedStatement pstmtSelect = (OraclePreparedStatement) this.connection.prepareStatement("select picture from ImageTour where id=" + id + " for update");

        try
        {
            OracleResultSet rset = (OracleResultSet) pstmtSelect.executeQuery();

            try
            {
                if (rset.next())
                {
                    imgProxy = (OrdImage) rset.getORAData("picture", OrdImage.getORADataFactory());
                }
            }
            finally
            {
                rset.close();
            }
        }
        finally
        {
            pstmtSelect.close();
        }

        return imgProxy;
    }

    /**
     * Load image from local file into the remote database
     * @param Absolute or relative path to the file saved as a string variable
     * @throws SQLException
     * @throws IOException
     */
    public void insertImageFromFile(String filename) throws SQLException, IOException
    {
        int id = this.getMaxId() + 1;
        boolean autoCommit = this.connection.getAutoCommit();
        this.connection.setAutoCommit(false);

        try
        {
            //  insert a new record with an empty ORDImage object
            OraclePreparedStatement pstmtInsert = (OraclePreparedStatement) this.connection.prepareStatement(
                    "insert into ImageTour(id, picture) values (" + id + ", ordsys.ordimage.init())");

            pstmtInsert.executeUpdate();
            pstmtInsert.close();

            OrdImage imgProxy = this.getProxy(id);

            //  load the media data from a file to the ORDImage Java object
            imgProxy.loadDataFromFile(filename);
            imgProxy.setProperties();

            OraclePreparedStatement pstmtUpdate1 = (OraclePreparedStatement) this.connection.prepareStatement(
                    "update ImageTour set picture = ? where id = " + id
            );

            try
            {
                pstmtUpdate1.setORAData(1, imgProxy);
                pstmtUpdate1.executeUpdate();
            }
            finally
            {
                pstmtUpdate1.close();
            }

            PreparedStatement pstmtUpdate2 = this.connection.prepareStatement(
                    "update ImageTour p set p.picture_si=SI_StillImage(p.picture.getContent()) where id = " + id
            );

            try
            {
                pstmtUpdate2.executeUpdate();
            }
            finally
            {
                pstmtUpdate2.close();
            }

            PreparedStatement pstmtUpdate3 = this.connection.prepareStatement(
                    "update ImageTour p set"+
                            " p.picture_ac=SI_AverageColor(p.picture_si),"+
                            " p.picture_ch=SI_ColorHistogram(p.picture_si),"+
                            " p.picture_pc=SI_PositionalColor(p.picture_si),"+
                            " p.picture_tx=SI_Texture(p.picture_si) where id = "+id
            );

            try
            {
                pstmtUpdate3.executeUpdate();
            }
            finally
            {
                pstmtUpdate3.close();
            }

            this.connection.commit();
        }
        finally
        {
            this.connection.setAutoCommit(autoCommit);
        }
    }

    /**
     * Update specific image saved in the remote database
     * @param Absolute or relative path to the file saved in local system
     * @param Integer index of image in the remote database
     * @throws SQLException
     * @throws IOException
     */
    public void updateImageFromFile(String filename, int id) throws SQLException, IOException
    {
        boolean autoCommit = this.connection.getAutoCommit();
        this.connection.setAutoCommit(false);

        try
        {
            OrdImage imgProxy = this.getProxy(id);

            // load the media data from a file to the ORDImage Java object
            imgProxy.loadDataFromFile(filename);
            imgProxy.setProperties();

            OraclePreparedStatement pstmtUpdate1 = (OraclePreparedStatement) this.connection.prepareStatement(
                    "update ImageTour set picture = ? where id = " + id
            );

            try
            {
                pstmtUpdate1.setORAData(1, imgProxy);
                pstmtUpdate1.executeUpdate();
            }
            finally
            {
                pstmtUpdate1.close();
            }

            PreparedStatement pstmtUpdate2 = this.connection.prepareStatement(
                    "update ImageTour p set p.picture_si=SI_StillImage(p.picture.getContent()) where id = " + id
            );

            try
            {
                pstmtUpdate2.executeUpdate();
            }
            finally
            {
                pstmtUpdate2.close();
            }

            PreparedStatement pstmtUpdate3 = this.connection.prepareStatement(
                    "update ImageTour p set"+
                            " p.picture_ac=SI_AverageColor(p.picture_si),"+
                            " p.picture_ch=SI_ColorHistogram(p.picture_si),"+
                            " p.picture_pc=SI_PositionalColor(p.picture_si),"+
                            " p.picture_tx=SI_Texture(p.picture_si) where id = "+id
            );

            try
            {
                pstmtUpdate3.executeUpdate();
            }
            finally
            {
                pstmtUpdate3.close();
            }

            this.connection.commit();
        }
        finally
        {
            this.connection.setAutoCommit(autoCommit);
        }
    }

    /**
     * Load image from the remote database
     * @param Integer index of appropriate image saved in remote database
     * @return Return image as JavaFX Image object
     * @throws SQLException
     * @throws IOException
     */
    public Image getImageFromDatabase(int id) throws SQLException, IOException
    {
        OrdImage imgProxy = this.getProxy(id);

        if (imgProxy == null)
        {
            return null;
        }

        BufferedImage bufferedImg = ImageIO.read(new ByteArrayInputStream(imgProxy.getDataInByteArray()));
        Image image = SwingFXUtils.toFXImage(bufferedImg, null);
        return image;
    }

    /**
     * Get number of images saved in the remote databse
     * @return Integer value which represents number of images
     * @throws SQLException
     */
    public int getMaxId() throws SQLException
    {
        int max = 0;

        OraclePreparedStatement pstmtSelect = (OraclePreparedStatement) this.connection.prepareStatement(
                "select MAX(id) as max from ImageTour"
        );

        OracleResultSet rset = (OracleResultSet) pstmtSelect.executeQuery();

        if (rset.next())
        {
            max = (int) rset.getInt("max");
        }

        rset.close();
        pstmtSelect.close();
        return max;
    }

    /**
     * Remove specific image from the remote database
     * @param Integer index of image
     * @throws SQLException
     */
    public void deleteImageById(int id) throws SQLException
    {
        OraclePreparedStatement pstmtSelect = (OraclePreparedStatement) this.connection.prepareStatement(
                "delete from ImageTour where id = " + id
        );

        pstmtSelect.executeQuery();
        pstmtSelect.close();
    }

    /**
     * Remove all images from the remote database
     * @throws SQLException
     */
    public void removeAllImages() throws SQLException
    {
        while (true)
        {
            int max = this.getMaxId();

            if (max > 0)
                this.deleteImageById(max);
            else
                break;
        }
    }

    /**
     * Return list of most similar images to the desired origin image
     * @param Integer index of desired image
     * @return Integer list of most similar images where first element is most similar image and last element is least similar image
     * @throws SQLException
     * @throws IOException
     */
    public List<Integer> similarity(int id) throws SQLException, IOException
    {
        List<Integer> similarityList = new ArrayList<Integer>();

        PreparedStatement pstmtSelect = connection.prepareStatement(
                "SELECT dst.*, SI_ScoreByFtrList(" +
                        "new SI_FeatureList(src.picture_ac,0.7,src.picture_ch,0.1,src.picture_pc,0.1,src.picture_tx,0.1),dst.picture_si)" +
                        " as similarity FROM ImageTour src, ImageTour dst " +
                        "WHERE (src.id <> dst.id) AND src.id = " + id +
                        " ORDER BY similarity ASC"
        );

        OracleResultSet rset = (OracleResultSet) pstmtSelect.executeQuery();

        while (rset.next())
        {
            similarityList.add(rset.getInt(1));
        }

        rset.close();
        pstmtSelect.close();
        return similarityList;
    }

}
