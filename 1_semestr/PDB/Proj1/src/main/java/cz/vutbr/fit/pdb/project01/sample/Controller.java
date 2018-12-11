package sample;

import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.HBox;

import java.awt.event.ActionEvent;
import java.awt.event.MouseEvent;
import java.io.*;
import java.sql.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.Date;

import javafx.stage.FileChooser;
import oracle.jdbc.OracleDriver;
import oracle.jdbc.pool.OracleDataSource;

/**
 * Enumeration which holds name of all tabs used in client application
 * @author Richard Hauerland
 */
enum tabType
{
    client,
    orders,
    tours,
    hotels,
    actions
}

/**
 * Class which allows easy manipulation with dates saved as a string values
 * @author Richard Hauerland
 */
class RichString
{
    /**
     * Convert number month to full name month in desired date string
     * @param Desired string value which holds date
     * @return String variable which holds date with month value saved as a full name in Czech language
     */
    static public String toRealDate(String content)
    {
        int N = content.length();
        String noSpace = "";

        for (int i = 0; i < N; i++)
        {
            if (content.charAt(i) == ' ' || content.charAt(i) == '\t' || content.charAt(i) == '\r' || content.charAt(i) == '\n')
            {
                //  pass
            }
            else
                noSpace = noSpace + content.charAt(i);
        }

        noSpace = noSpace.replaceFirst("[-]12[-]", ". prosince ");
        noSpace = noSpace.replaceFirst("[-]11[-]", ". listopadu ");
        noSpace = noSpace.replaceFirst("[-]10[-]", ". října ");
        noSpace = noSpace.replaceFirst("[-]09[-]", ". září ");
        noSpace = noSpace.replaceFirst("[-]08[-]", ". srpna ");
        noSpace = noSpace.replaceFirst("[-]07[-]", ". července ");
        noSpace = noSpace.replaceFirst("[-]06[-]", ". června ");
        noSpace = noSpace.replaceFirst("[-]05[-]", ". května ");
        noSpace = noSpace.replaceFirst("[-]04[-]", ". dubna ");
        noSpace = noSpace.replaceFirst("[-]03[-]", ". března ");
        noSpace = noSpace.replaceFirst("[-]02[-]", ". února ");
        noSpace = noSpace.replaceFirst("[-]01[-]", ". ledna ");

        return noSpace;
    }

    /**
     * Return actual date
     * @param String date as one and only parameter
     * @return Return actual date saved as a LocalDate object
     */
    static public final LocalDate stringDate(String dateString)
    {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy");
        LocalDate localDate = LocalDate.parse(dateString, formatter);
        return localDate;
    }

    /**
     * Chronological compare of two dates
     * @param Desired date saved as a string variable
     * @param Second date saved as a string variable
     * @return Boolean which tells if desired date is chronologically before second date
     * @throws ParseException
     */
    static public boolean isDateBefore(String firstDate, String secondDate) throws ParseException
    {
        SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy");

        Date first;
        Date second;

        try
        {
            first = sdf.parse(firstDate);
            second = sdf.parse(secondDate);

            if (first.before(second))
                return true;
        }
        catch(ParseException ex)
        {
            //  pass
        }

        return false;
    }
}

/**
 * User class which has got same structure as a table in our SQL database
 * @author Richard Hauerland
 */
class ConceptUser
{
    /**
     * Class attribute variable
     */
    public String login = "";

    /**
     * Class attribute variable
     */
    public String password = "";

    /**
     * Class attribute variable
     */
    public String firstName = "";

    /**
     * Class attribute variable
     */
    public String lastName = "";

    /**
     * Class attribute variable
     */
    public boolean isMale = true;

    /**
     * Class attribute variable
     */
    public String identificationNumber = "";

    /**
     * Class attribute variable
     */
    public String birthDate = "";

    /**
     * Class attribute variable
     */
    public String phone = "";

    /**
     * Class attribute variable
     */
    public String email = "";

    /**
     * Class attribute variable
     */
    public String address = "";

    /**
     * Class attribute variable
     */
    public int ID_user = 0;

    /**
     * Class attribute variable
     */
    public String begining = "";

    /**
     * Class attribute variable
     */
    public String ending = "";
}

/**
 * Hotel class which has got same structure as a table in our SQL database
 * @author Richard Hauerland
 */
class ConceptHotel
{
    /**
     * Class attribute variable
     */
    public int ID_hotel = 0;

    /**
     * Class attribute variable
     */
    public String name = "";

    /**
     * Class attribute variable
     */
    public int stars = 4;
}

/**
 * Action class which has got same structure as a table in our SQL database
 * @author Richard Hauerland
 */
class ConceptAction
{
    /**
     * Class attribute variable
     */
    public int ID_action = 0;

    /**
     * Class attribute variable
     */
    public String type = "";

    /**
     * Class attribute variable
     */
    public int persons = 10;

    /**
     * Class attribute variable
     */
    public String from = "";

    /**
     * Class attribute variable
     */
    public String to = "";
}

/**
 * Tour class which has got same structure as a table in our SQL database
 * @author Richard Hauerland
 */
class ConceptTour
{
    /**
     * Class attribute variable
     */
    public int ID_tour = 0;

    /**
     * Class attribute variable
     */
    public String state = "";

    /**
     * Class attribute variable
     */
    public String location = "";

    /**
     * Class attribute variable
     */
    public String center = "";

    /**
     * Class attribute variable
     */
    public String from = "";

    /**
     * Class attribute variable
     */
    public String to = "";

    /**
     * Class attribute variable
     */
    public int ID_hotel = 0;
}

/**
 * Order class which has got same structure as a table in our SQL database
 * @author Richard Hauerland
 */
class ConceptOrder
{
    /**
     * Class attribute variable
     */
    public int ID_order = 0;

    /**
     * Class attribute variable
     */
    public boolean accepted = true;

    /**
     * Class attribute variable
     */
    public boolean cancelled = false;

    /**
     * Class attribute variable
     */
    public String date = "";

    /**
     * Class attribute variable
     */
    public String begining = "";

    /**
     * Class attribute variable
     */
    public String ending = "";
}

class ConceptOrderUser
{
    /**
     * Class attribute variable
     */
    public int ID_order_user = 0;

    /**
     * Class attribute variable
     */
    public int ID_user = 0;

    /**
     * Class attribute variable
     */
    public int ID_order = 0;

    /**
     * Class attribute variable
     */
    public String begining = "";

    /**
     * Class attribute variable
     */
    public String ending = "";
}

/**
 * Tour order class which has got same structure as a table in our SQL database
 * @author Richard Hauerland
 */
class ConceptOrderTour
{
    /**
     * Class attribute variable
     */
    public int ID_order_tour = 0;

    /**
     * Class attribute variable
     */
    public int ID_order = 0;

    /**
     * Class attribute variable
     */
    public int ID_tour = 0;

    /**
     * Class attribute variable
     */
    public boolean food = true;

    /**
     * Class attribute variable
     */
    public boolean bus = false;

    /**
     * Class attribute variable
     */
    public int persons = 2;
}

/**
 * Action order class which has got same structure as a table in our SQL database
 * @author Richard Hauerland
 */
class ConceptOrderAction
{
    /**
     * Class attribute variable
     */
    public int ID_order_action = 0;

    /**
     * Class attribute variable
     */
    public int ID_order_tour = 0;

    /**
     * Class attribute variable
     */
    public int ID_action = 0;

    /**
     * Class attribute variable
     */
    public boolean food = true;

    /**
     * Class attribute variable
     */
    public boolean bus = false;

    /**
     * Class attribute variable
     */
    public int persons = 2;
}

/**
 * Backend class which represents storage of hotel
 * @author Richard Hauerland
 */
class Hotel
{
    /**
     * Class attribute variable
     */
    public String name = "Hotel Grand";

    /**
     * Class attribute variable
     */
    public int stars = 5;
}

/**
 * Backend class which represents storage of tour
 * @author Richard Hauerland
 */
class Tour
{
    /**
     * Class attribute variable
     */
    public String state = "Rakousko";

    /**
     * Class attribute variable
     */
    public String location = "Innsbruck";

    /**
     * Class attribute variable
     */
    public String center = "Kleinberg";

    /**
     * Class attribute variable
     */
    public String from = "01-01-2018";

    /**
     * Class attribute variable
     */
    public String to = "14-01-2018";

    /**
     * Class attribute variable
     */
    boolean food = true;

    /**
     * Class attribute variable
     */
    boolean bus = false;

    /**
     * Class attribute variable
     */
    public Hotel hotel = new Hotel();
}

/**
 * Backend class which represents storage of action
 * @author Richard Hauerland
 */
class Action
{
    /**
     * Class attribute variable
     */
    public String name = "Grilování";

    /**
     * Class attribute variable
     */
    public int persons = 10;

    /**
     * Class attribute variable
     */
    public String from = "01-01-2018";

    /**
     * Class attribute variable
     */
    public String to = "31-12-2018";

    /**
     * Class attribute variable
     */
    boolean want = false;
}

/**
 * Backend class which represents storage of order
 * @author Richard Hauerland
 */
class Order
{
    /**
     * Class attribute variable
     */
    public int tourIndex = 0;

    /**
     * Class attribute variable
     */
    public List<Integer> actionsIndices = new ArrayList<Integer>();

    /**
     * Class attribute variable
     */
    boolean food = true;

    /**
     * Class attribute variable
     */
    boolean bus = false;

    /**
     * Class attribute variable
     */
    public int personCount = 2;
}

/**
 * Backend class which represents storage of order pack
 * @author Richard Hauerland
 */
class OrderPack
{
    /**
     * Class attribute variable
     */
    public List<Order> orders = new ArrayList<Order>();

    /**
     * Class attribute variable
     */
    public String orderDate = "01-01-2018";

    /**
     * Class attribute variable
     */
    public boolean accepted = false;

    /**
     * Class attribute variable
     */
    public boolean cancelled = false;
}

/**
 * Backend class which represents storage of user
 * @author Richard Hauerland
 */
class User
{
    /**
     * Class attribute variable
     */
    public String username = "defaultLogin";

    /**
     * Class attribute variable
     */
    public String password = "mypassword";

    /**
     * Class attribute variable
     */
    public String firstName = "David";

    /**
     * Class attribute variable
     */
    public String lastName = "Smith";

    /**
     * Class attribute variable
     */
    public String identificationNumber = "9301016789";

    /**
     * Class attribute variable
     */
    public boolean isMale = true;

    /**
     * Class attribute variable
     */
    public String birthDate = "01-01-1993";

    /**
     * Class attribute variable
     */
    public String phoneNumber = "123456789";

    /**
     * Class attribute variable
     */
    public String email = "defaultLogin@gmail.com";

    /**
     * Class attribute variable
     */
    public String address = "Los Angeles, Burbank, 1st Avenue, 42";

    /**
     * Class attribute variable
     */
    public int ID_user = 0;

    /**
     * Class attribute variable
     */
    public String begining = "";

    /**
     * Class attribute variable
     */
    public String ending = "";

    /**
     * Class attribute variable
     */
    List<OrderPack> orders = new ArrayList<OrderPack>();                //  every user has got separated list of orders
}

/**
 * Backbone class which implements the biggest part of client application
 * @author Richard Hauerland
 */
public class Controller
{
    /**
     * Java backend variable
     */
    String databaseLogin = "xhauer02";

    /**
     * Java backend variable
     */
    String databasePassword = "SoX2T7E1";

    /**
     * Java backend variable
     */
    int databaseLoads = 0;

    /**
     * Java backend variable
     */
    int ordersCount = 0;

    /**
     * Java backend variable
     */
    int orderToursCount = 0;

    /**
     * Java backend variable
     */
    int orderActionsCount = 0;

    /**
     * Java backend variable
     */
    int orderTourProcedure = -1;

    /**
     * Java backend variable
     */
    int orderHotelProcedure = -1;

    /**
     * Java backend variable
     */
    int loggedIn = 0;

    /**
     * Java backend variable
     */
    boolean adminLogged = false;

    /**
     * Java backend variable
     */
    boolean pageChangeAllowed = true;

    /**
     * Java backend variable
     */
    tabType actualTab = tabType.client;

    /**
     * Java backend variable
     */
    int ordersPageIndex = 0;

    /**
     * Java backend variable
     */
    int toursPageIndex = 0;

    /**
     * Java backend variable
     */
    int hotelsPageIndex = 0;

    /**
     * Java backend variable
     */
    int actionsPageIndex = 0;

    /**
     * Java backend variable
     */
    boolean similarityActive = false;

    /**
     * Java backend variable
     */
    List<Tour> toursRestore = new ArrayList<Tour>();

    /**
     * Java backend variable
     */
    List<Hotel> hotelsRestore = new ArrayList<Hotel>();

    /**
     * Java backend variable
     */
    List<User> users = new ArrayList<User>();

    /**
     * Java backend variable
     */
    List<Tour> tours = new ArrayList<Tour>();

    /**
     * Java backend variable
     */
    List<Hotel> hotels = new ArrayList<Hotel>();

    /**
     * Java backend variable
     */
    List<Action> actions = new ArrayList<Action>();

    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TABS
    /**
     * JavaFX graphical element
     */
    @FXML
    private TabPane tabs;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tab clientTab;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tab ordersTab;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tab toursTab;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tab hotelsTab;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tab actionsTab;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - SCROLL PANES
    /**
     * JavaFX graphical element
     */
    @FXML
    private ScrollPane ordersScrollPane;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ScrollPane toursScrollPane;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ScrollPane hotelsScrollPane;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ScrollPane actionsScrollPane;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - LOGIN PAGE
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox account;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView accountImage;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button imagePathButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button imageRotateLeftButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button imageRotateRightButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tooltip imageRotateRightTooltip;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button imageContrastDownButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button imageContrastUpButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button imageBrightnessDownButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button imageBrightnessUpButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tooltip imageRemoveTooltip;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField loginEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private PasswordField passwordEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox nameBox;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField firstNameEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField lastNameEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField identificationNumberEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button genderButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox genderBox;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField phoneEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private DatePicker birthEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox numberBox;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField emailEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField addressEdit;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button acceptButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button logoutButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button adminButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tooltip acceptTooltip;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Tooltip logoutTooltip;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER ONE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorOne;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER TWO BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorTwo;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER THREE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorThree;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER FOUR BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorFour;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER FIVE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorFive;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER SIX BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorSix;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER SEVEN BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorSeven;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER EIGHT BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorEight;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER NINE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator orderSeparatorNine;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ORDER TEN BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox orderTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView orderImageTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderDateTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderTourSelectTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourStateTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourLocationTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderTourCenterTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderFromLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderToLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderHotelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderServicesTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label orderMembersCountTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ComboBox orderActionsTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button orderAcceptTen;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR ONE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorOne;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR TWO BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorTwo;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR THREE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorThree;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR FOUR BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorFour;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR FIVE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorFive;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR SIX BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorSix;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR SEVEN BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonSeven;


    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorSeven;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR EIGHT BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorEight;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR NINE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonNine;


    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator tourSeparatorNine;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - TOUR TEN BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox tourTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView tourImageTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label stateLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label locationLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label centerLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label fromLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label toLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox foodCheckTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox busCheckTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickTourButtonTen;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL ONE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorOne;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL TWO TWO
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorTwo;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL THREE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorThree;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL FOUR BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorFour;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL FIVE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorFive;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL SIX BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorSix;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL SEVEN BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorSeven;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL EIGHT BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorEight;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL NINE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator hotelSeparatorNine;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - HOTEL TEN BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox hotelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView hotelImageTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label hotelLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView starsImageTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button pickHotelButtonTen;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION ONE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckOne;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorOne;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION TWO BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckTwo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorTwo;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION THREE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckThree;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorThree;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION FOUR BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckFour;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorFour;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION FIVE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckFive;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorFive;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION SIX BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckSix;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorSix;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION SEVEN BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckSeven;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorSeven;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION EIGHT BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckEight;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorEight;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION NINE BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckNine;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Separator actionSeparatorNine;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTION TEN BOX
    /**
     * JavaFX graphical element
     */
    @FXML
    private HBox actionTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private ImageView actionImageTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label personsLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionFromLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Label actionToLabelTen;

    /**
     * JavaFX graphical element
     */
    @FXML
    private CheckBox actionCheckTen;
    //  - - - - - - - - - - - - - - - - - - - - - - - - - - - BOTTOM TASK BAR
    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField filterState;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField filterLocation;

    /**
     * JavaFX graphical element
     */
    @FXML
    private TextField filterCenter;

    /**
     * JavaFX graphical element
     */
    @FXML
    private DatePicker filterFrom;

    /**
     * JavaFX graphical element
     */
    @FXML
    private DatePicker filterTo;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button similarityButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Spinner personSpinner;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Button insertButton;

    /**
     * JavaFX graphical element
     */
    @FXML
    private Spinner pageSpinner;

    /**
     * Execute administrator initialization of database content and set database to its default state
     */
    @FXML
    private void adminDatabaseInit()
    {
        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {

                    try
                    {
                        Scanner read = new Scanner (new File("src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/sql/init.sql"));
                        read.useDelimiter(";");
                        String chunk = "";

                        while (read.hasNext())
                        {
                            chunk = read.next();

                            while (chunk.startsWith("\n") || chunk.startsWith("\t") || chunk.startsWith(" "))
                            {
                                chunk = chunk.substring(1, chunk.length());
                            }

                            while (chunk.endsWith("\n") || chunk.endsWith("\t") || chunk.endsWith(" "))
                            {
                                chunk = chunk.substring(0, chunk.length() - 1);
                            }

                            if (chunk.length() > 5)
                            {
                                stmt.addBatch(chunk);
                            }
                        }

                        read.close();
                    }
                    catch (FileNotFoundException fnfe)
                    {
                        //  pass
                    }

                    stmt.executeBatch();
                }

            } // close the connection
        } catch (SQLException sqlEx) {
            System.err.println("SQLException: " + sqlEx.getMessage());
        }

        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {

                    try
                    {
                        Scanner read = new Scanner (new File("src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/sql/procedures.sql"));
                        read.useDelimiter("/");
                        String chunk = "";

                        while (read.hasNext())
                        {
                            chunk = read.next();

                            while (chunk.startsWith("\n") || chunk.startsWith("\t") || chunk.startsWith(" "))
                            {
                                chunk = chunk.substring(1, chunk.length());
                            }

                            while (chunk.endsWith("\n") || chunk.endsWith("\t") || chunk.endsWith(" "))
                            {
                                chunk = chunk.substring(0, chunk.length() - 1);
                            }

                            if (chunk.length() > 5)
                            {
                                stmt.executeLargeUpdate(chunk);
                            }
                        }

                        read.close();
                    }
                    catch (FileNotFoundException fnfe)
                    {
                        //  pass
                    }
                }

            } // close the connection
        } catch (SQLException sqlEx) {
            System.err.println("SQLException: " + sqlEx.getMessage());
        }

        try
        {
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            try (Connection conn = ods.getConnection()) {

                multimedia.ImageIdentity identityPictures = new multimedia.ImageIdentity(conn);
                identityPictures.removeAllImages();

                for (int i = 1; i <= 4; i++)
                    identityPictures.insertImageFromFile("src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/identity" + i + ".png");

                multimedia.ImageTour tourPictures = new multimedia.ImageTour(conn);
                tourPictures.removeAllImages();

                for (int i = 1; i <= 12; i++)
                    tourPictures.insertImageFromFile("src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour" + i + ".gif");

                multimedia.ImageHotel hotelPictures = new multimedia.ImageHotel(conn);
                hotelPictures.removeAllImages();

                for (int i = 1; i <= 12; i++)
                    hotelPictures.insertImageFromFile("src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel" + i + ".gif");

                multimedia.ImageAction actionPictures = new multimedia.ImageAction(conn);
                actionPictures.removeAllImages();

                for (int i = 1; i <= 11; i++)
                    actionPictures.insertImageFromFile("src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action" + i + ".gif");
            }
        }
        catch (Exception ex)
        {
            System.out.println(ex.getMessage());
        }
    }

    /**
     * Find appropriate index of restore tour by setting row index
     * @param Index of tours row
     * @return Appropriate index of restore tour
     */
    @FXML
    private int findTourInRestore(int rowIndex)
    {
        int index = toursPageIndex * 10 + rowIndex;
        int N = toursRestore.size();

        for (int i = 0; i < N; i++)
        {
            if (tours.get(index).state.equalsIgnoreCase(toursRestore.get(i).state) &&
                tours.get(index).location.equalsIgnoreCase(toursRestore.get(i).location) &&
                tours.get(index).center.equalsIgnoreCase(toursRestore.get(i).center) &&
                tours.get(index).from.equalsIgnoreCase(toursRestore.get(i).from) &&
                tours.get(index).to.equalsIgnoreCase(toursRestore.get(i).to))
            {
                return i;
            }
        }

        return -1;
    }

    /**
     * Find appropriate index of restore hotel by setting row index
     * @param Index of hotels row
     * @return Appropriate index of restore hotel
     */
    @FXML
    private int findHotelInRestore(int rowIndex)
    {
        int index = hotelsPageIndex * 10 + rowIndex;
        int N = hotelsRestore.size();

        for (int i = 0; i < N; i++)
        {
            if (hotels.get(index).name.equalsIgnoreCase(hotelsRestore.get(i).name) && (hotels.get(index).stars == hotelsRestore.get(i).stars))
            {
                return i;
            }
        }

        return -1;
    }

    /**
     * Refresh content of all order boxes inside orders tab
     */
    @FXML
    private void updateOrders()
    {
        if (loggedIn < 0)
            return;

        List<OrderPack> orders = users.get(loggedIn).orders;

        int N = orders.size();

        if (N > (ordersPageIndex * 10 + 0))                     //  order box one
        {
            if (orderOne.isVisible() == false)
            {
                orderOne.setVisible(true);
                orderOne.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 0).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 0).cancelled)
                {
                    orderAcceptOne.setVisible(false);
                    orderAcceptOne.setManaged(false);

                    orderImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptOne.setText("Zrušit");
                    orderAcceptOne.setVisible(true);
                    orderAcceptOne.setManaged(true);

                    orderImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptOne.setText("Potvrdit");
                orderAcceptOne.setVisible(true);
                orderAcceptOne.setManaged(true);

                orderImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateOne.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 0).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 0).orders.size();
            orderTourSelectOne.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectOne.getItems().add("Zájezd " + (i + 1));

            orderTourSelectOne.getSelectionModel().select(0);
            orderTourSelected(0, 0);
        }
        else if (orderOne.isVisible())
        {
            orderOne.setVisible(false);
            orderOne.setManaged(false);

            orderAcceptOne.setVisible(false);
            orderAcceptOne.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 1))                     //  order box two
        {
            if (orderTwo.isVisible() == false)
            {
                orderTwo.setVisible(true);
                orderTwo.setManaged(true);

                orderSeparatorOne.setVisible(true);
                orderSeparatorOne.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 1).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 1).cancelled)
                {
                    orderAcceptTwo.setVisible(false);
                    orderAcceptTwo.setManaged(false);

                    orderImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptTwo.setText("Zrušit");
                    orderAcceptTwo.setVisible(true);
                    orderAcceptTwo.setManaged(true);

                    orderImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptTwo.setText("Potvrdit");
                orderAcceptTwo.setVisible(true);
                orderAcceptTwo.setManaged(true);

                orderImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateTwo.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 1).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 1).orders.size();
            orderTourSelectTwo.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectTwo.getItems().add("Zájezd " + (i + 1));

            orderTourSelectTwo.getSelectionModel().select(0);
            orderTourSelected(1, 0);
        }
        else if (orderTwo.isVisible())
        {
            orderTwo.setVisible(false);
            orderTwo.setManaged(false);

            orderAcceptTwo.setVisible(false);
            orderAcceptTwo.setManaged(false);

            orderSeparatorOne.setVisible(false);
            orderSeparatorOne.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 2))                     //  order box three
        {
            if (orderThree.isVisible() == false)
            {
                orderThree.setVisible(true);
                orderThree.setManaged(true);

                orderSeparatorTwo.setVisible(true);
                orderSeparatorTwo.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 2).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 2).cancelled)
                {
                    orderAcceptThree.setVisible(false);
                    orderAcceptThree.setManaged(false);

                    orderImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptThree.setText("Zrušit");
                    orderAcceptThree.setVisible(true);
                    orderAcceptThree.setManaged(true);

                    orderImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptThree.setText("Potvrdit");
                orderAcceptThree.setVisible(true);
                orderAcceptThree.setManaged(true);

                orderImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateThree.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 2).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 2).orders.size();
            orderTourSelectThree.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectThree.getItems().add("Zájezd " + (i + 1));

            orderTourSelectThree.getSelectionModel().select(0);
            orderTourSelected(2, 0);
        }
        else if (orderThree.isVisible())
        {
            orderThree.setVisible(false);
            orderThree.setManaged(false);

            orderAcceptThree.setVisible(false);
            orderAcceptThree.setManaged(false);

            orderSeparatorTwo.setVisible(false);
            orderSeparatorTwo.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 3))                     //  order box four
        {
            if (orderFour.isVisible() == false)
            {
                orderFour.setVisible(true);
                orderFour.setManaged(true);

                orderSeparatorThree.setVisible(true);
                orderSeparatorThree.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 3).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 3).cancelled)
                {
                    orderAcceptFour.setVisible(false);
                    orderAcceptFour.setManaged(false);

                    orderImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptFour.setText("Zrušit");
                    orderAcceptFour.setVisible(true);
                    orderAcceptFour.setManaged(true);

                    orderImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptFour.setText("Potvrdit");
                orderAcceptFour.setVisible(true);
                orderAcceptFour.setManaged(true);

                orderImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateFour.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 3).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 3).orders.size();
            orderTourSelectFour.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectFour.getItems().add("Zájezd " + (i + 1));

            orderTourSelectFour.getSelectionModel().select(0);
            orderTourSelected(3, 0);
        }
        else if (orderFour.isVisible())
        {
            orderFour.setVisible(false);
            orderFour.setManaged(false);

            orderAcceptFour.setVisible(false);
            orderAcceptFour.setManaged(false);

            orderSeparatorThree.setVisible(false);
            orderSeparatorThree.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 4))                     //  order box five
        {
            if (orderFive.isVisible() == false)
            {
                orderFive.setVisible(true);
                orderFive.setManaged(true);

                orderSeparatorFour.setVisible(true);
                orderSeparatorFour.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 4).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 4).cancelled)
                {
                    orderAcceptFive.setVisible(false);
                    orderAcceptFive.setManaged(false);

                    orderImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptFive.setText("Zrušit");
                    orderAcceptFive.setVisible(true);
                    orderAcceptFive.setManaged(true);

                    orderImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptFive.setText("Potvrdit");
                orderAcceptFive.setVisible(true);
                orderAcceptFive.setManaged(true);

                orderImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateFive.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 4).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 4).orders.size();
            orderTourSelectFive.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectFive.getItems().add("Zájezd " + (i + 1));

            orderTourSelectFive.getSelectionModel().select(0);
            orderTourSelected(4, 0);
        }
        else if (orderFive.isVisible())
        {
            orderFive.setVisible(false);
            orderFive.setManaged(false);

            orderAcceptFive.setVisible(false);
            orderAcceptFive.setManaged(false);

            orderSeparatorFour.setVisible(false);
            orderSeparatorFour.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 5))                     //  order box six
        {
            if (orderSix.isVisible() == false)
            {
                orderSix.setVisible(true);
                orderSix.setManaged(true);

                orderSeparatorFive.setVisible(true);
                orderSeparatorFive.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 5).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 5).cancelled)
                {
                    orderAcceptSix.setVisible(false);
                    orderAcceptSix.setManaged(false);

                    orderImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptSix.setText("Zrušit");
                    orderAcceptSix.setVisible(true);
                    orderAcceptSix.setManaged(true);

                    orderImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptSix.setText("Potvrdit");
                orderAcceptSix.setVisible(true);
                orderAcceptSix.setManaged(true);

                orderImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateSix.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 5).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 5).orders.size();
            orderTourSelectSix.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectSix.getItems().add("Zájezd " + (i + 1));

            orderTourSelectSix.getSelectionModel().select(0);
            orderTourSelected(5, 0);
        }
        else if (orderSix.isVisible())
        {
            orderSix.setVisible(false);
            orderSix.setManaged(false);

            orderAcceptSix.setVisible(false);
            orderAcceptSix.setManaged(false);

            orderSeparatorFive.setVisible(false);
            orderSeparatorFive.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 6))                     //  order box seven
        {
            if (orderSeven.isVisible() == false)
            {
                orderSeven.setVisible(true);
                orderSeven.setManaged(true);

                orderSeparatorSix.setVisible(true);
                orderSeparatorSix.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 6).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 6).cancelled)
                {
                    orderAcceptSeven.setVisible(false);
                    orderAcceptSeven.setManaged(false);

                    orderImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptSeven.setText("Zrušit");
                    orderAcceptSeven.setVisible(true);
                    orderAcceptSeven.setManaged(true);

                    orderImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptSeven.setText("Potvrdit");
                orderAcceptSeven.setVisible(true);
                orderAcceptSeven.setManaged(true);

                orderImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateSeven.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 6).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 6).orders.size();
            orderTourSelectSeven.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectSeven.getItems().add("Zájezd " + (i + 1));

            orderTourSelectSeven.getSelectionModel().select(0);
            orderTourSelected(6, 0);
        }
        else if (orderSeven.isVisible())
        {
            orderSeven.setVisible(false);
            orderSeven.setManaged(false);

            orderAcceptSeven.setVisible(false);
            orderAcceptSeven.setManaged(false);

            orderSeparatorSix.setVisible(false);
            orderSeparatorSix.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 7))                     //  order box eight
        {
            if (orderEight.isVisible() == false)
            {
                orderEight.setVisible(true);
                orderEight.setManaged(true);

                orderSeparatorSeven.setVisible(true);
                orderSeparatorSeven.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 7).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 7).cancelled)
                {
                    orderAcceptEight.setVisible(false);
                    orderAcceptEight.setManaged(false);

                    orderImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptEight.setText("Zrušit");
                    orderAcceptEight.setVisible(true);
                    orderAcceptEight.setManaged(true);

                    orderImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptEight.setText("Potvrdit");
                orderAcceptEight.setVisible(true);
                orderAcceptEight.setManaged(true);

                orderImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateEight.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 7).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 7).orders.size();
            orderTourSelectEight.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectEight.getItems().add("Zájezd " + (i + 1));

            orderTourSelectEight.getSelectionModel().select(0);
            orderTourSelected(7, 0);
        }
        else if (orderEight.isVisible())
        {
            orderEight.setVisible(false);
            orderEight.setManaged(false);

            orderAcceptEight.setVisible(false);
            orderAcceptEight.setManaged(false);

            orderSeparatorSeven.setVisible(false);
            orderSeparatorSeven.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 8))                     //  order box nine
        {
            if (orderNine.isVisible() == false)
            {
                orderNine.setVisible(true);
                orderNine.setManaged(true);

                orderSeparatorEight.setVisible(true);
                orderSeparatorEight.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 8).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 8).cancelled)
                {
                    orderAcceptNine.setVisible(false);
                    orderAcceptNine.setManaged(false);

                    orderImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptNine.setText("Zrušit");
                    orderAcceptNine.setVisible(true);
                    orderAcceptNine.setManaged(true);

                    orderImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptNine.setText("Potvrdit");
                orderAcceptNine.setVisible(true);
                orderAcceptNine.setManaged(true);

                orderImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateNine.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 8).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 8).orders.size();
            orderTourSelectNine.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectNine.getItems().add("Zájezd " + (i + 1));

            orderTourSelectNine.getSelectionModel().select(0);
            orderTourSelected(8, 0);
        }
        else if (orderNine.isVisible())
        {
            orderNine.setVisible(false);
            orderNine.setManaged(false);

            orderAcceptNine.setVisible(false);
            orderAcceptNine.setManaged(false);

            orderSeparatorEight.setVisible(false);
            orderSeparatorEight.setManaged(false);
        }

        if (N > (ordersPageIndex * 10 + 9))                     //  order box ten
        {
            if (orderTen.isVisible() == false)
            {
                orderTen.setVisible(true);
                orderTen.setManaged(true);

                orderSeparatorNine.setVisible(true);
                orderSeparatorNine.setManaged(true);
            }

            if (orders.get(ordersPageIndex * 10 + 9).accepted)
            {
                if (orders.get(ordersPageIndex * 10 + 9).cancelled)
                {
                    orderAcceptTen.setVisible(false);
                    orderAcceptTen.setManaged(false);

                    orderImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
                }
                else
                {
                    orderAcceptTen.setText("Zrušit");
                    orderAcceptTen.setVisible(true);
                    orderAcceptTen.setManaged(true);

                    orderImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
                }
            }
            else
            {
                orderAcceptTen.setText("Potvrdit");
                orderAcceptTen.setVisible(true);
                orderAcceptTen.setManaged(true);

                orderImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/box.png"));
            }

            orderDateTen.setText(RichString.toRealDate(orders.get(ordersPageIndex * 10 + 9).orderDate));
            int M = orders.get(ordersPageIndex * 10 + 9).orders.size();
            orderTourSelectTen.getItems().clear();

            for (int i = 0; i < M; i++)
                orderTourSelectTen.getItems().add("Zájezd " + (i + 1));

            orderTourSelectTen.getSelectionModel().select(0);
            orderTourSelected(9, 0);
        }
        else if (orderTen.isVisible())
        {
            orderTen.setVisible(false);
            orderTen.setManaged(false);

            orderAcceptTen.setVisible(false);
            orderAcceptTen.setManaged(false);

            orderSeparatorNine.setVisible(false);
            orderSeparatorNine.setManaged(false);
        }

        ordersScrollPane.setVvalue(0.0);
    }

    /**
     * Refresh content of all tour boxes inside tours tab
     */
    @FXML
    private void updateTours()
    {
        int N = tours.size();

        if (N > (toursPageIndex * 10 + 0))
        {
            if (tourOne.isVisible() == false)
            {
                tourOne.setVisible(true);
                tourOne.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(0);

                    if (index < pictures.getMaxId())
                        tourImageOne.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelOne.setText(tours.get(toursPageIndex * 10 + 0).state);
            locationLabelOne.setText(tours.get(toursPageIndex * 10 + 0).location);
            centerLabelOne.setText(tours.get(toursPageIndex * 10 + 0).center);
            fromLabelOne.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 0).from));
            toLabelOne.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 0).to));
            foodCheckOne.setSelected(tours.get(toursPageIndex * 10 + 0).food);
            busCheckOne.setSelected(tours.get(toursPageIndex * 10 + 0).bus);
        }
        else if (tourOne.isVisible())
        {
            tourOne.setVisible(false);
            tourOne.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 1))
        {
            if (tourTwo.isVisible() == false)
            {
                tourTwo.setVisible(true);
                tourTwo.setManaged(true);

                tourSeparatorOne.setVisible(true);
                tourSeparatorOne.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(1);

                    if (index < pictures.getMaxId())
                        tourImageTwo.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelTwo.setText(tours.get(toursPageIndex * 10 + 1).state);
            locationLabelTwo.setText(tours.get(toursPageIndex * 10 + 1).location);
            centerLabelTwo.setText(tours.get(toursPageIndex * 10 + 1).center);
            fromLabelTwo.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 1).from));
            toLabelTwo.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 1).to));
            foodCheckTwo.setSelected(tours.get(toursPageIndex * 10 + 1).food);
            busCheckTwo.setSelected(tours.get(toursPageIndex * 10 + 1).bus);
        }
        else if (tourTwo.isVisible())
        {
            tourTwo.setVisible(false);
            tourTwo.setManaged(false);

            tourSeparatorOne.setVisible(false);
            tourSeparatorOne.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 2))
        {
            if (tourThree.isVisible() == false)
            {
                tourThree.setVisible(true);
                tourThree.setManaged(true);

                tourSeparatorTwo.setVisible(true);
                tourSeparatorTwo.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(2);

                    if (index < pictures.getMaxId())
                        tourImageThree.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelThree.setText(tours.get(toursPageIndex * 10 + 2).state);
            locationLabelThree.setText(tours.get(toursPageIndex * 10 + 2).location);
            centerLabelThree.setText(tours.get(toursPageIndex * 10 + 2).center);
            fromLabelThree.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 2).from));
            toLabelThree.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 2).to));
            foodCheckThree.setSelected(tours.get(toursPageIndex * 10 + 2).food);
            busCheckThree.setSelected(tours.get(toursPageIndex * 10 + 2).bus);
        }
        else if (tourThree.isVisible())
        {
            tourThree.setVisible(false);
            tourThree.setManaged(false);

            tourSeparatorTwo.setVisible(false);
            tourSeparatorTwo.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 3))
        {
            if (tourFour.isVisible() == false)
            {
                tourFour.setVisible(true);
                tourFour.setManaged(true);

                tourSeparatorThree.setVisible(true);
                tourSeparatorThree.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(3);

                    if (index < pictures.getMaxId())
                        tourImageFour.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelFour.setText(tours.get(toursPageIndex * 10 + 3).state);
            locationLabelFour.setText(tours.get(toursPageIndex * 10 + 3).location);
            centerLabelFour.setText(tours.get(toursPageIndex * 10 + 3).center);
            fromLabelFour.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 3).from));
            toLabelFour.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 3).to));
            foodCheckFour.setSelected(tours.get(toursPageIndex * 10 + 3).food);
            busCheckFour.setSelected(tours.get(toursPageIndex * 10 + 3).bus);
        }
        else if (tourFour.isVisible())
        {
            tourFour.setVisible(false);
            tourFour.setManaged(false);

            tourSeparatorThree.setVisible(false);
            tourSeparatorThree.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 4))
        {
            if (tourFive.isVisible() == false)
            {
                tourFive.setVisible(true);
                tourFive.setManaged(true);

                tourSeparatorFour.setVisible(true);
                tourSeparatorFour.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(4);

                    if (index < pictures.getMaxId())
                        tourImageFive.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelFive.setText(tours.get(toursPageIndex * 10 + 4).state);
            locationLabelFive.setText(tours.get(toursPageIndex * 10 + 4).location);
            centerLabelFive.setText(tours.get(toursPageIndex * 10 + 4).center);
            fromLabelFive.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 4).from));
            toLabelFive.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 4).to));
            foodCheckFive.setSelected(tours.get(toursPageIndex * 10 + 4).food);
            busCheckFive.setSelected(tours.get(toursPageIndex * 10 + 4).bus);
        }
        else if (tourFive.isVisible())
        {
            tourFive.setVisible(false);
            tourFive.setManaged(false);

            tourSeparatorFour.setVisible(false);
            tourSeparatorFour.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 5))
        {
            if (tourSix.isVisible() == false)
            {
                tourSix.setVisible(true);
                tourSix.setManaged(true);

                tourSeparatorFive.setVisible(true);
                tourSeparatorFive.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(5);

                    if (index < pictures.getMaxId())
                        tourImageSix.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelSix.setText(tours.get(toursPageIndex * 10 + 5).state);
            locationLabelSix.setText(tours.get(toursPageIndex * 10 + 5).location);
            centerLabelSix.setText(tours.get(toursPageIndex * 10 + 5).center);
            fromLabelSix.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 5).from));
            toLabelSix.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 5).to));
            foodCheckSix.setSelected(tours.get(toursPageIndex * 10 + 5).food);
            busCheckSix.setSelected(tours.get(toursPageIndex * 10 + 5).bus);
        }
        else if (tourSix.isVisible())
        {
            tourSix.setVisible(false);
            tourSix.setManaged(false);

            tourSeparatorFive.setVisible(false);
            tourSeparatorFive.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 6))
        {
            if (tourSeven.isVisible() == false)
            {
                tourSeven.setVisible(true);
                tourSeven.setManaged(true);

                tourSeparatorSix.setVisible(true);
                tourSeparatorSix.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(6);

                    if (index < pictures.getMaxId())
                        tourImageSeven.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelSeven.setText(tours.get(toursPageIndex * 10 + 6).state);
            locationLabelSeven.setText(tours.get(toursPageIndex * 10 + 6).location);
            centerLabelSeven.setText(tours.get(toursPageIndex * 10 + 6).center);
            fromLabelSeven.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 6).from));
            toLabelSeven.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 6).to));
            foodCheckSeven.setSelected(tours.get(toursPageIndex * 10 + 6).food);
            busCheckSeven.setSelected(tours.get(toursPageIndex * 10 + 6).bus);
        }
        else if (tourSeven.isVisible())
        {
            tourSeven.setVisible(false);
            tourSeven.setManaged(false);

            tourSeparatorSix.setVisible(false);
            tourSeparatorSix.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 7))
        {
            if (tourEight.isVisible() == false)
            {
                tourEight.setVisible(true);
                tourEight.setManaged(true);

                tourSeparatorSeven.setVisible(true);
                tourSeparatorSeven.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(7);

                    if (index < pictures.getMaxId())
                        tourImageEight.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelEight.setText(tours.get(toursPageIndex * 10 + 7).state);
            locationLabelEight.setText(tours.get(toursPageIndex * 10 + 7).location);
            centerLabelEight.setText(tours.get(toursPageIndex * 10 + 7).center);
            fromLabelEight.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 7).from));
            toLabelEight.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 7).to));
            foodCheckEight.setSelected(tours.get(toursPageIndex * 10 + 7).food);
            busCheckEight.setSelected(tours.get(toursPageIndex * 10 + 7).bus);
        }
        else if (tourEight.isVisible())
        {
            tourEight.setVisible(false);
            tourEight.setManaged(false);

            tourSeparatorSeven.setVisible(false);
            tourSeparatorSeven.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 8))
        {
            if (tourNine.isVisible() == false)
            {
                tourNine.setVisible(true);
                tourNine.setManaged(true);

                tourSeparatorEight.setVisible(true);
                tourSeparatorEight.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(8);

                    if (index < pictures.getMaxId())
                        tourImageNine.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelNine.setText(tours.get(toursPageIndex * 10 + 8).state);
            locationLabelNine.setText(tours.get(toursPageIndex * 10 + 8).location);
            centerLabelNine.setText(tours.get(toursPageIndex * 10 + 8).center);
            fromLabelNine.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 8).from));
            toLabelNine.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 8).to));
            foodCheckNine.setSelected(tours.get(toursPageIndex * 10 + 8).food);
            busCheckNine.setSelected(tours.get(toursPageIndex * 10 + 8).bus);
        }
        else if (tourNine.isVisible())
        {
            tourNine.setVisible(false);
            tourNine.setManaged(false);

            tourSeparatorEight.setVisible(false);
            tourSeparatorEight.setManaged(false);
        }

        if (N > (toursPageIndex * 10 + 9))
        {
            if (tourTen.isVisible() == false)
            {
                tourTen.setVisible(true);
                tourTen.setManaged(true);

                tourSeparatorNine.setVisible(true);
                tourSeparatorNine.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                    int index = findTourInRestore(9);

                    if (index < pictures.getMaxId())
                        tourImageTen.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        tourImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/tour1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            stateLabelTen.setText(tours.get(toursPageIndex * 10 + 9).state);
            locationLabelTen.setText(tours.get(toursPageIndex * 10 + 9).location);
            centerLabelTen.setText(tours.get(toursPageIndex * 10 + 9).center);
            fromLabelTen.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 9).from));
            toLabelTen.setText(RichString.toRealDate(tours.get(toursPageIndex * 10 + 9).to));
            foodCheckTen.setSelected(tours.get(toursPageIndex * 10 + 9).food);
            busCheckTen.setSelected(tours.get(toursPageIndex * 10 + 9).bus);
        }
        else if (tourTen.isVisible())
        {
            tourTen.setVisible(false);
            tourTen.setManaged(false);

            tourSeparatorNine.setVisible(false);
            tourSeparatorNine.setManaged(false);
        }

        toursScrollPane.setVvalue(0.0);
    }

    /**
     * Initialize tours to default state and fill relative tours list
     */
    @FXML
    private void initTours()
    {
        tours.clear();
        int M = toursRestore.size();

        for (int i = 0; i < M; i++)
        {
            boolean found = false;
            int N = tours.size();

            for (int j = 0; j < N; j++)
            {
                if (tours.get(j).state.equalsIgnoreCase(toursRestore.get(i).state) && tours.get(j).location.equalsIgnoreCase(toursRestore.get(i).location) &&
                    tours.get(j).center.equalsIgnoreCase(toursRestore.get(i).center) && tours.get(j).from.equalsIgnoreCase(toursRestore.get(i).from) &&
                    tours.get(j).to.equalsIgnoreCase(toursRestore.get(i).to))
                {
                    found = true;
                    break;
                }
            }

            if (found == false)
                tours.add(toursRestore.get(i));
        }

        updateTours();
    }

    /**
     * Refresh content of all hotel boxes inside hotels tab
     */
    @FXML
    private void updateHotels()
    {
        int N = hotels.size();

        if (N > (hotelsPageIndex * 10 + 0))
        {
            if (hotelOne.isVisible() == false)
            {
                hotelOne.setVisible(true);
                hotelOne.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(0);

                    if (index < pictures.getMaxId())
                        hotelImageOne.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelOne.setText(hotels.get(hotelsPageIndex * 10 + 0).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 0).stars;

            if (starsCount == 1)
                starsImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelOne.isVisible())
        {
            hotelOne.setVisible(false);
            hotelOne.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 1))
        {
            if (hotelTwo.isVisible() == false)
            {
                hotelTwo.setVisible(true);
                hotelTwo.setManaged(true);

                hotelSeparatorOne.setVisible(true);
                hotelSeparatorOne.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(1);

                    if (index < pictures.getMaxId())
                        hotelImageTwo.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelTwo.setText(hotels.get(hotelsPageIndex * 10 + 1).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 1).stars;

            if (starsCount == 1)
                starsImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelTwo.isVisible())
        {
            hotelTwo.setVisible(false);
            hotelTwo.setManaged(false);

            hotelSeparatorOne.setVisible(false);
            hotelSeparatorOne.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 2))
        {
            if (hotelThree.isVisible() == false)
            {
                hotelThree.setVisible(true);
                hotelThree.setManaged(true);

                hotelSeparatorTwo.setVisible(true);
                hotelSeparatorTwo.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(2);

                    if (index < pictures.getMaxId())
                        hotelImageThree.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelThree.setText(hotels.get(hotelsPageIndex * 10 + 2).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 2).stars;

            if (starsCount == 1)
                starsImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelThree.isVisible())
        {
            hotelThree.setVisible(false);
            hotelThree.setManaged(false);

            hotelSeparatorTwo.setVisible(false);
            hotelSeparatorTwo.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 3))
        {
            if (hotelFour.isVisible() == false)
            {
                hotelFour.setVisible(true);
                hotelFour.setManaged(true);

                hotelSeparatorThree.setVisible(true);
                hotelSeparatorThree.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(3);

                    if (index < pictures.getMaxId())
                        hotelImageFour.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelFour.setText(hotels.get(hotelsPageIndex * 10 + 3).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 3).stars;

            if (starsCount == 1)
                starsImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelFour.isVisible())
        {
            hotelFour.setVisible(false);
            hotelFour.setManaged(false);

            hotelSeparatorThree.setVisible(false);
            hotelSeparatorThree.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 4))
        {
            if (hotelFive.isVisible() == false)
            {
                hotelFive.setVisible(true);
                hotelFive.setManaged(true);

                hotelSeparatorFour.setVisible(true);
                hotelSeparatorFour.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(4);

                    if (index < pictures.getMaxId())
                        hotelImageFive.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelFive.setText(hotels.get(hotelsPageIndex * 10 + 4).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 4).stars;

            if (starsCount == 1)
                starsImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelFive.isVisible())
        {
            hotelFive.setVisible(false);
            hotelFive.setManaged(false);

            hotelSeparatorFour.setVisible(false);
            hotelSeparatorFour.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 5))
        {
            if (hotelSix.isVisible() == false)
            {
                hotelSix.setVisible(true);
                hotelSix.setManaged(true);

                hotelSeparatorFive.setVisible(true);
                hotelSeparatorFive.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(5);

                    if (index < pictures.getMaxId())
                        hotelImageSix.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelSix.setText(hotels.get(hotelsPageIndex * 10 + 5).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 5).stars;

            if (starsCount == 1)
                starsImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelSix.isVisible())
        {
            hotelSix.setVisible(false);
            hotelSix.setManaged(false);

            hotelSeparatorFive.setVisible(false);
            hotelSeparatorFive.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 6))
        {
            if (hotelSeven.isVisible() == false)
            {
                hotelSeven.setVisible(true);
                hotelSeven.setManaged(true);

                hotelSeparatorSix.setVisible(true);
                hotelSeparatorSix.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(6);

                    if (index < pictures.getMaxId())
                        hotelImageSeven.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelSeven.setText(hotels.get(hotelsPageIndex * 10 + 6).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 6).stars;

            if (starsCount == 1)
                starsImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelSeven.isVisible())
        {
            hotelSeven.setVisible(false);
            hotelSeven.setManaged(false);

            hotelSeparatorSix.setVisible(false);
            hotelSeparatorSix.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 7))
        {
            if (hotelEight.isVisible() == false)
            {
                hotelEight.setVisible(true);
                hotelEight.setManaged(true);

                hotelSeparatorSeven.setVisible(true);
                hotelSeparatorSeven.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(7);

                    if (index < pictures.getMaxId())
                        hotelImageEight.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelEight.setText(hotels.get(hotelsPageIndex * 10 + 7).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 7).stars;

            if (starsCount == 1)
                starsImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelEight.isVisible())
        {
            hotelEight.setVisible(false);
            hotelEight.setManaged(false);

            hotelSeparatorSeven.setVisible(false);
            hotelSeparatorSeven.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 8))
        {
            if (hotelNine.isVisible() == false)
            {
                hotelNine.setVisible(true);
                hotelNine.setManaged(true);

                hotelSeparatorEight.setVisible(true);
                hotelSeparatorEight.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(8);

                    if (index < pictures.getMaxId())
                        hotelImageNine.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelNine.setText(hotels.get(hotelsPageIndex * 10 + 8).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 8).stars;

            if (starsCount == 1)
                starsImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelNine.isVisible())
        {
            hotelNine.setVisible(false);
            hotelNine.setManaged(false);

            hotelSeparatorEight.setVisible(false);
            hotelSeparatorEight.setManaged(false);
        }

        if (N > (hotelsPageIndex * 10 + 9))
        {
            if (hotelTen.isVisible() == false)
            {
                hotelTen.setVisible(true);
                hotelTen.setManaged(true);

                hotelSeparatorNine.setVisible(true);
                hotelSeparatorNine.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageHotel pictures = new multimedia.ImageHotel(conn);
                    int index = findHotelInRestore(9);

                    if (index < pictures.getMaxId())
                        hotelImageTen.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        hotelImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/hotel1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            hotelLabelTen.setText(hotels.get(hotelsPageIndex * 10 + 9).name);

            int starsCount = hotels.get(hotelsPageIndex * 10 + 9).stars;

            if (starsCount == 1)
                starsImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/oneStar.png"));
            else if (starsCount == 2)
                starsImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/twoStar.png"));
            else if (starsCount == 3)
                starsImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/threeStar.png"));
            else if (starsCount == 4)
                starsImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fourStar.png"));
            else if (starsCount == 5)
                starsImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/fiveStar.png"));
        }
        else if (hotelTen.isVisible())
        {
            hotelTen.setVisible(false);
            hotelTen.setManaged(false);

            hotelSeparatorNine.setVisible(false);
            hotelSeparatorNine.setManaged(false);
        }

        hotelsScrollPane.setVvalue(0.0);
    }

    /**
     * Initialize hotels to default state and fill relative hotels list
     */
    @FXML
    private void initHotels()
    {
        updateHotels();
    }

    /**
     * Refresh content of all action boxes inside actions tab
     */
    @FXML
    private void updateActions()
    {
        int N = actions.size();

        if (N > (actionsPageIndex * 10 + 0))
        {
            if (actionOne.isVisible() == false)
            {
                actionOne.setVisible(true);
                actionOne.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 0;

                    if (index < pictures.getMaxId())
                        actionImageOne.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelOne.setText(actions.get(actionsPageIndex * 10 + 0).name);

            int persons = actions.get(actionsPageIndex * 10 + 0).persons;

            if (persons == 1)
                personsLabelOne.setText("1 osoba");
            else if (persons == 2)
                personsLabelOne.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelOne.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelOne.setText("Až 4 osoby");
            else
                personsLabelOne.setText("Až " + persons + " osob");

            actionFromLabelOne.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 0).from));
            actionToLabelOne.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 0).to));
            actionCheckOne.setSelected(actions.get(actionsPageIndex * 10 + 0).want);
        }
        else if (actionOne.isVisible())
        {
            actionOne.setVisible(false);
            actionOne.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 1))
        {
            if (actionTwo.isVisible() == false)
            {
                actionTwo.setVisible(true);
                actionTwo.setManaged(true);

                actionSeparatorOne.setVisible(true);
                actionSeparatorOne.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 1;

                    if (index < pictures.getMaxId())
                        actionImageTwo.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelTwo.setText(actions.get(actionsPageIndex * 10 + 1).name);

            int persons = actions.get(actionsPageIndex * 10 + 1).persons;

            if (persons == 1)
                personsLabelTwo.setText("1 osoba");
            else if (persons == 2)
                personsLabelTwo.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelTwo.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelTwo.setText("Až 4 osoby");
            else
                personsLabelTwo.setText("Až " + persons + " osob");

            actionFromLabelTwo.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 1).from));
            actionToLabelTwo.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 1).to));
            actionCheckTwo.setSelected(actions.get(actionsPageIndex * 10 + 1).want);
        }
        else if (actionTwo.isVisible())
        {
            actionTwo.setVisible(false);
            actionTwo.setManaged(false);

            actionSeparatorOne.setVisible(false);
            actionSeparatorOne.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 2))
        {
            if (actionThree.isVisible() == false)
            {
                actionThree.setVisible(true);
                actionThree.setManaged(true);

                actionSeparatorTwo.setVisible(true);
                actionSeparatorTwo.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 2;

                    if (index < pictures.getMaxId())
                        actionImageThree.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelThree.setText(actions.get(actionsPageIndex * 10 + 2).name);

            int persons = actions.get(actionsPageIndex * 10 + 2).persons;

            if (persons == 1)
                personsLabelThree.setText("1 osoba");
            else if (persons == 2)
                personsLabelThree.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelThree.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelThree.setText("Až 4 osoby");
            else
                personsLabelThree.setText("Až " + persons + " osob");

            actionFromLabelThree.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 2).from));
            actionToLabelThree.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 2).to));
            actionCheckThree.setSelected(actions.get(actionsPageIndex * 10 + 2).want);
        }
        else if (actionThree.isVisible())
        {
            actionThree.setVisible(false);
            actionThree.setManaged(false);

            actionSeparatorTwo.setVisible(false);
            actionSeparatorTwo.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 3))
        {
            if (actionFour.isVisible() == false)
            {
                actionFour.setVisible(true);
                actionFour.setManaged(true);

                actionSeparatorThree.setVisible(true);
                actionSeparatorThree.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 3;

                    if (index < pictures.getMaxId())
                        actionImageFour.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelFour.setText(actions.get(actionsPageIndex * 10 + 3).name);

            int persons = actions.get(actionsPageIndex * 10 + 3).persons;

            if (persons == 1)
                personsLabelFour.setText("1 osoba");
            else if (persons == 2)
                personsLabelFour.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelFour.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelFour.setText("Až 4 osoby");
            else
                personsLabelFour.setText("Až " + persons + " osob");

            actionFromLabelFour.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 3).from));
            actionToLabelFour.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 3).to));
            actionCheckFour.setSelected(actions.get(actionsPageIndex * 10 + 3).want);
        }
        else if (actionFour.isVisible())
        {
            actionFour.setVisible(false);
            actionFour.setManaged(false);

            actionSeparatorThree.setVisible(false);
            actionSeparatorThree.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 4))
        {
            if (actionFive.isVisible() == false)
            {
                actionFive.setVisible(true);
                actionFive.setManaged(true);

                actionSeparatorFour.setVisible(true);
                actionSeparatorFour.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 4;

                    if (index < pictures.getMaxId())
                        actionImageFive.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelFive.setText(actions.get(actionsPageIndex * 10 + 4).name);

            int persons = actions.get(actionsPageIndex * 10 + 4).persons;

            if (persons == 1)
                personsLabelFive.setText("1 osoba");
            else if (persons == 2)
                personsLabelFive.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelFive.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelFive.setText("Až 4 osoby");
            else
                personsLabelFive.setText("Až " + persons + " osob");

            actionFromLabelFive.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 4).from));
            actionToLabelFive.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 4).to));
            actionCheckFive.setSelected(actions.get(actionsPageIndex * 10 + 4).want);
        }
        else if (actionFive.isVisible())
        {
            actionFive.setVisible(false);
            actionFive.setManaged(false);

            actionSeparatorFour.setVisible(false);
            actionSeparatorFour.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 5))
        {
            if (actionSix.isVisible() == false)
            {
                actionSix.setVisible(true);
                actionSix.setManaged(true);

                actionSeparatorFive.setVisible(true);
                actionSeparatorFive.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 5;

                    if (index < pictures.getMaxId())
                        actionImageSix.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelSix.setText(actions.get(actionsPageIndex * 10 + 5).name);

            int persons = actions.get(actionsPageIndex * 10 + 5).persons;

            if (persons == 1)
                personsLabelSix.setText("1 osoba");
            else if (persons == 2)
                personsLabelSix.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelSix.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelSix.setText("Až 4 osoby");
            else
                personsLabelSix.setText("Až " + persons + " osob");

            actionFromLabelSix.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 5).from));
            actionToLabelSix.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 5).to));
            actionCheckSix.setSelected(actions.get(actionsPageIndex * 10 + 5).want);
        }
        else if (actionSix.isVisible())
        {
            actionSix.setVisible(false);
            actionSix.setManaged(false);

            actionSeparatorFive.setVisible(false);
            actionSeparatorFive.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 6))
        {
            if (actionSeven.isVisible() == false)
            {
                actionSeven.setVisible(true);
                actionSeven.setManaged(true);

                actionSeparatorSix.setVisible(true);
                actionSeparatorSix.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 6;

                    if (index < pictures.getMaxId())
                        actionImageSeven.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelSeven.setText(actions.get(actionsPageIndex * 10 + 6).name);

            int persons = actions.get(actionsPageIndex * 10 + 6).persons;

            if (persons == 1)
                personsLabelSeven.setText("1 osoba");
            else if (persons == 2)
                personsLabelSeven.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelSeven.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelSeven.setText("Až 4 osoby");
            else
                personsLabelSeven.setText("Až " + persons + " osob");

            actionFromLabelSeven.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 6).from));
            actionToLabelSeven.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 6).to));
            actionCheckSeven.setSelected(actions.get(actionsPageIndex * 10 + 6).want);
        }
        else if (actionSeven.isVisible())
        {
            actionSeven.setVisible(false);
            actionSeven.setManaged(false);

            actionSeparatorSix.setVisible(false);
            actionSeparatorSix.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 7))
        {
            if (actionEight.isVisible() == false)
            {
                actionEight.setVisible(true);
                actionEight.setManaged(true);

                actionSeparatorSeven.setVisible(true);
                actionSeparatorSeven.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 7;

                    if (index < pictures.getMaxId())
                        actionImageEight.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelEight.setText(actions.get(actionsPageIndex * 10 + 7).name);

            int persons = actions.get(actionsPageIndex * 10 + 7).persons;

            if (persons == 1)
                personsLabelEight.setText("1 osoba");
            else if (persons == 2)
                personsLabelEight.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelEight.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelEight.setText("Až 4 osoby");
            else
                personsLabelEight.setText("Až " + persons + " osob");

            actionFromLabelEight.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 7).from));
            actionToLabelEight.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 7).to));
            actionCheckEight.setSelected(actions.get(actionsPageIndex * 10 + 7).want);
        }
        else if (actionEight.isVisible())
        {
            actionEight.setVisible(false);
            actionEight.setManaged(false);

            actionSeparatorSeven.setVisible(false);
            actionSeparatorSeven.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 8))
        {
            if (actionNine.isVisible() == false)
            {
                actionNine.setVisible(true);
                actionNine.setManaged(true);

                actionSeparatorEight.setVisible(true);
                actionSeparatorEight.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 8;

                    if (index < pictures.getMaxId())
                        actionImageNine.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelNine.setText(actions.get(actionsPageIndex * 10 + 8).name);

            int persons = actions.get(actionsPageIndex * 10 + 8).persons;

            if (persons == 1)
                personsLabelNine.setText("1 osoba");
            else if (persons == 2)
                personsLabelNine.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelNine.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelNine.setText("Až 4 osoby");
            else
                personsLabelNine.setText("Až " + persons + " osob");

            actionFromLabelNine.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 8).from));
            actionToLabelNine.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 8).to));
            actionCheckNine.setSelected(actions.get(actionsPageIndex * 10 + 8).want);
        }
        else if (actionNine.isVisible())
        {
            actionNine.setVisible(false);
            actionNine.setManaged(false);

            actionSeparatorEight.setVisible(false);
            actionSeparatorEight.setManaged(false);
        }

        if (N > (actionsPageIndex * 10 + 9))
        {
            if (actionTen.isVisible() == false)
            {
                actionTen.setVisible(true);
                actionTen.setManaged(true);

                actionSeparatorNine.setVisible(true);
                actionSeparatorNine.setManaged(true);
            }

            try
            {
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                try (Connection conn = ods.getConnection()) {

                    multimedia.ImageAction pictures = new multimedia.ImageAction(conn);
                    int index = actionsPageIndex * 10 + 9;

                    if (index < pictures.getMaxId())
                        actionImageTen.setImage(pictures.getImageFromDatabase(index + 1));
                    else
                        actionImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/in/action1.gif"));
                }
            }
            catch (Exception ex)
            {
                System.out.println(ex.getMessage());
            }

            actionLabelTen.setText(actions.get(actionsPageIndex * 10 + 9).name);

            int persons = actions.get(actionsPageIndex * 10 + 9).persons;

            if (persons == 1)
                personsLabelTen.setText("1 osoba");
            else if (persons == 2)
                personsLabelTen.setText("Až 2 osoby");
            else if (persons == 3)
                personsLabelTen.setText("Až 3 osoby");
            else if (persons == 4)
                personsLabelTen.setText("Až 4 osoby");
            else
                personsLabelTen.setText("Až " + persons + " osob");

            actionFromLabelTen.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 9).from));
            actionToLabelTen.setText(RichString.toRealDate(actions.get(actionsPageIndex * 10 + 9).to));
            actionCheckTen.setSelected(actions.get(actionsPageIndex * 10 + 9).want);
        }
        else if (actionTen.isVisible())
        {
            actionTen.setVisible(false);
            actionTen.setManaged(false);

            actionSeparatorNine.setVisible(false);
            actionSeparatorNine.setManaged(false);
        }

        actionsScrollPane.setVvalue(0.0);
    }

    /**
     * Initialize actions to default state and fill relative actions list
     */
    @FXML
    private void initActions()
    {
        updateActions();
    }

    /**
     * Check login information and execute user login inside client if success
     */
    @FXML
    private void handleLogin()
    {
        if (loggedIn >= 0)
        {
            accountImage.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/key.png"));

            acceptButton.setText("Registrace");
            logoutButton.setText("Přihlásit");
            acceptTooltip.setText("Přejít na stránku registrace");
            logoutTooltip.setText("Přihlášení do systému");

            loginEdit.setEditable(true);

            passwordEdit.clear();

            nameBox.setVisible(false);
            nameBox.setManaged(false);

            genderBox.setVisible(false);
            genderBox.setManaged(false);

            numberBox.setVisible(false);
            numberBox.setManaged(false);

            emailEdit.setVisible(false);
            emailEdit.setManaged(false);

            addressEdit.setVisible(false);
            addressEdit.setManaged(false);

            imagePathButton.setVisible(false);
            imagePathButton.setManaged(false);

            imageRotateLeftButton.setVisible(false);
            imageRotateLeftButton.setManaged(false);

            imageRotateRightButton.setVisible(false);
            imageRotateRightButton.setManaged(false);

            imageContrastDownButton.setVisible(false);
            imageContrastDownButton.setManaged(false);

            imageContrastUpButton.setVisible(false);
            imageContrastUpButton.setManaged(false);

            imageBrightnessDownButton.setVisible(false);
            imageBrightnessDownButton.setManaged(false);

            imageBrightnessUpButton.setVisible(false);
            imageBrightnessUpButton.setManaged(false);

            ordersTab.setDisable(true);

            loggedIn = -1;
        }
        else if (loggedIn == -1)
        {
            int N = users.size();
            boolean found = false;

            for (int i = 0; i < N; i++)
            {
                if (loginEdit.getText().equalsIgnoreCase(users.get(i).username) && passwordEdit.getText().equals(users.get(i).password))
                {
                    if (loginEdit.getText().equalsIgnoreCase("Admin"))
                    {
                        loginEdit.setText("Administrátor");
                        loginEdit.setEditable(false);

                        passwordEdit.setVisible(false);
                        passwordEdit.setManaged(false);

                        logoutButton.setVisible(false);
                        logoutButton.setManaged(false);

                        acceptButton.setVisible(false);
                        acceptButton.setManaged(false);

                        imageRotateRightButton.setVisible(true);
                        imageRotateRightButton.setManaged(true);
                        imageRotateRightTooltip.setText("Iniciální naplnění databáze");

                        adminButton.setText("Odhlásit");
                        adminLogged = true;
                        return;
                    }

                    loginEdit.setText(users.get(i).username);
                    passwordEdit.setText(users.get(i).password);
                    firstNameEdit.setText(users.get(i).firstName);
                    lastNameEdit.setText(users.get(i).lastName);
                    identificationNumberEdit.setText(users.get(i).identificationNumber);

                    if (users.get(i).isMale)
                        genderButton.setText("Muž");
                    else
                        genderButton.setText("Žena");

                    birthEdit.setValue(RichString.stringDate(users.get(i).birthDate));
                    phoneEdit.setText(users.get(i).phoneNumber);
                    emailEdit.setText(users.get(i).email);
                    addressEdit.setText(users.get(i).address);

                    loggedIn = i;
                    found = true;

                    break;
                }
            }

            if (found)
            {
                acceptButton.setText("Potvrdit");
                logoutButton.setText("Odhlásit");
                acceptTooltip.setText("Potvrzení provedených změn");
                logoutTooltip.setText("Odhlášení uživatele");

                loginEdit.setEditable(false);

                nameBox.setVisible(true);
                nameBox.setManaged(true);

                genderBox.setVisible(true);
                genderBox.setManaged(true);

                numberBox.setVisible(true);
                numberBox.setManaged(true);

                emailEdit.setVisible(true);
                emailEdit.setManaged(true);

                addressEdit.setVisible(true);
                addressEdit.setManaged(true);

                acceptButton.requestFocus();

                imagePathButton.setVisible(true);
                imagePathButton.setManaged(true);

                imageRotateLeftButton.setVisible(true);
                imageRotateLeftButton.setManaged(true);

                imageRotateRightButton.setVisible(true);
                imageRotateRightButton.setManaged(true);

                imageContrastDownButton.setVisible(true);
                imageContrastDownButton.setManaged(true);

                imageContrastUpButton.setVisible(true);
                imageContrastUpButton.setManaged(true);

                imageBrightnessDownButton.setVisible(true);
                imageBrightnessDownButton.setManaged(true);

                imageBrightnessUpButton.setVisible(true);
                imageBrightnessUpButton.setManaged(true);

                ordersTab.setDisable(false);

                try
                {
                    OracleDataSource ods = new OracleDataSource();
                    ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                    ods.setUser(databaseLogin);
                    ods.setPassword(databasePassword);

                    try (Connection conn = ods.getConnection()) {

                        multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);

                        if (loggedIn < pictures.getMaxId())
                            accountImage.setImage(pictures.getImageFromDatabase(loggedIn + 1));
                        else
                            accountImage.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/warning.png"));
                    }
                }
                catch (Exception ex)
                {
                    System.out.println(ex.getMessage());
                }

                updateOrders();
            }
        }
        else
        {
            acceptButton.setText("Registrace");
            logoutButton.setText("Přihlásit");
            acceptTooltip.setText("Přejít na stránku registrace");
            logoutTooltip.setText("Přihlášení do systému");

            loginEdit.setEditable(true);
            loginEdit.setStyle("-fx-text-fill: black;");

            passwordEdit.clear();

            nameBox.setVisible(false);
            nameBox.setManaged(false);

            genderBox.setVisible(false);
            genderBox.setManaged(false);

            numberBox.setVisible(false);
            numberBox.setManaged(false);

            emailEdit.setVisible(false);
            emailEdit.setManaged(false);

            addressEdit.setVisible(false);
            addressEdit.setManaged(false);

            ordersTab.setDisable(true);

            loggedIn = -1;
        }
    }

    /**
     * Check all user attributes and save changes into the remote database
     */
    @FXML
    private void handleUserUpdate()
    {
        if (loggedIn >= 0)
        {
            if (passwordEdit.getText().length() > 0)
            {
                if (firstNameEdit.getText().length() > 0)
                {
                    if (lastNameEdit.getText().length() > 0)
                    {
                        if (identificationNumberEdit.getText().length() > 0)
                        {
                            if (phoneEdit.getText().length() > 0)
                            {
                                if (emailEdit.getText().length() > 0)
                                {
                                    if (addressEdit.getText().length() > 0)
                                    {
                                        if (identificationNumberEdit.getText().length() == 10 && identificationNumberEdit.getText().matches("[0-9]+"))
                                        {
                                            //  pass
                                        }
                                        else
                                        {
                                            identificationNumberEdit.setStyle("-fx-text-fill: red;");
                                            return;
                                        }

                                        if (phoneEdit.getText().length() == 9 && phoneEdit.getText().matches("[0-9]+"))
                                        {
                                            //  pass
                                        }
                                        else
                                        {
                                            phoneEdit.setStyle("-fx-text-fill: red;");
                                            return;
                                        }

                                        if (emailEdit.getText().matches("[A-Za-z0-9]+[@][A-Za-z0-9]+[.][a-z]+"))
                                        {
                                            //  pass
                                        }
                                        else
                                        {
                                            emailEdit.setStyle("-fx-text-fill: red;");
                                            return;
                                        }

                                        identificationNumberEdit.setStyle("-fx-text-fill: black;");
                                        phoneEdit.setStyle("-fx-text-fill: black;");
                                        emailEdit.setStyle("-fx-text-fill: black;");

                                        users.get(loggedIn).password = passwordEdit.getText();
                                        users.get(loggedIn).firstName = firstNameEdit.getText();
                                        users.get(loggedIn).lastName = lastNameEdit.getText();
                                        users.get(loggedIn).identificationNumber = identificationNumberEdit.getText();

                                        if (genderButton.getText().equalsIgnoreCase("Muž"))
                                            users.get(loggedIn).isMale = true;
                                        else
                                            users.get(loggedIn).isMale = false;

                                        users.get(loggedIn).phoneNumber = phoneEdit.getText();
                                        users.get(loggedIn).birthDate = birthEdit.getValue().format(DateTimeFormatter.ofPattern("dd-MM-yyyy"));
                                        users.get(loggedIn).email = emailEdit.getText();
                                        users.get(loggedIn).address = addressEdit.getText();

                                        try {
                                            // create a OracleDataSource instance
                                            OracleDataSource ods = new OracleDataSource();
                                            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                                            ods.setUser(databaseLogin);
                                            ods.setPassword(databasePassword);

                                            char gender = 'F';

                                            if (users.get(loggedIn).isMale)
                                                gender = 'M';

                                            Timestamp ts = new Timestamp(System.currentTimeMillis());
                                            Date date = new Date();
                                            date.setTime(ts.getTime());
                                            String formattedDate = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss").format(date);

                                            int userID = -1;

                                            // connect to the database
                                            try (Connection conn = ods.getConnection()) {
                                                // create a Statement
                                                try (Statement stmt = conn.createStatement()) {
                                                    String command = "SELECT ID_user FROM klient WHERE login = '" + users.get(loggedIn).username + "'";

                                                    // select something from the system's dual table
                                                    try (ResultSet rset = stmt.executeQuery(command)) {
                                                        // iterate through the result and print the values
                                                        while (rset.next()) {
                                                            userID = Integer.parseInt(rset.getObject(1).toString());
                                                        }
                                                    } // close the ResultSet
                                                } // close the Statement
                                            } // close the connection

                                            String userCommand = "UPDATE klient SET " +
                                                    "heslo = '" + users.get(loggedIn).password + "', " +
                                                    "jmeno = '" + users.get(loggedIn).firstName + "', " +
                                                    "prijmeni = '" + users.get(loggedIn).lastName + "', " +
                                                    "pohlavi = '" + gender + "', " +
                                                    "rodne_cislo = " + users.get(loggedIn).identificationNumber + ", " +
                                                    "datum_narozeni = '" + users.get(loggedIn).birthDate + "', " +
                                                    "telefon = " + users.get(loggedIn).phoneNumber + ", " +
                                                    "email = '" + users.get(loggedIn).email + "', " +
                                                    "adresa = '" + users.get(loggedIn).address + "', " +
                                                    "ID_user = " + userID + ", " +
                                                    "begining = TO_DATE('" + formattedDate + "', 'DD-MM-YYYY HH24:MI:SS') " +
                                                    "WHERE login = '" + users.get(loggedIn).username + "'";

                                            // connect to the database
                                            try (Connection conn = ods.getConnection()) {
                                                // create a Statement
                                                try (Statement stmt = conn.createStatement()) {
                                                    stmt.executeUpdate(userCommand);
                                                } // close the Statement
                                            } // close the connection
                                        } catch (SQLException sqlEx) {
                                            System.err.println("SQLException: " + sqlEx.getMessage());
                                        }
                                    }
                                    else
                                    {
                                        addressEdit.requestFocus();
                                    }
                                }
                                else
                                {
                                    emailEdit.requestFocus();
                                }
                            }
                            else
                            {
                                phoneEdit.requestFocus();
                            }
                        }
                        else
                        {
                            identificationNumberEdit.requestFocus();
                        }
                    }
                    else
                    {
                        lastNameEdit.requestFocus();
                    }
                }
                else
                {
                    firstNameEdit.requestFocus();
                }
            }
            else
            {
                passwordEdit.requestFocus();
            }
        }
        else if (loggedIn == -1)
        {
            acceptButton.setText("Registrace");
            logoutButton.setText("Zrušit");
            acceptTooltip.setText("Provést registraci");
            logoutTooltip.setText("Ukončení procesu registrace");

            loginEdit.clear();
            passwordEdit.clear();
            firstNameEdit.clear();
            lastNameEdit.clear();
            identificationNumberEdit.clear();
            genderButton.setText("Muž");
            phoneEdit.clear();
            birthEdit.setValue(RichString.stringDate("01-01-1993"));
            emailEdit.clear();
            addressEdit.clear();

            nameBox.setVisible(true);
            nameBox.setManaged(true);

            genderBox.setVisible(true);
            genderBox.setManaged(true);

            numberBox.setVisible(true);
            numberBox.setManaged(true);

            emailEdit.setVisible(true);
            emailEdit.setManaged(true);

            addressEdit.setVisible(true);
            addressEdit.setManaged(true);

            acceptButton.requestFocus();

            loggedIn = -2;
        }
        else
        {
            if (passwordEdit.getText().length() > 0)
            {
                if (firstNameEdit.getText().length() > 0)
                {
                    if (lastNameEdit.getText().length() > 0)
                    {
                        if (identificationNumberEdit.getText().length() > 0)
                        {
                            if (phoneEdit.getText().length() > 0)
                            {
                                if (emailEdit.getText().length() > 0)
                                {
                                    if (addressEdit.getText().length() > 0)
                                    {
                                        if (identificationNumberEdit.getText().length() == 10 && identificationNumberEdit.getText().matches("[0-9]+"))
                                        {
                                            //  pass
                                        }
                                        else
                                        {
                                            identificationNumberEdit.setStyle("-fx-text-fill: red;");
                                            return;
                                        }

                                        if (phoneEdit.getText().length() == 9 && phoneEdit.getText().matches("[0-9]+"))
                                        {
                                            //  pass
                                        }
                                        else
                                        {
                                            phoneEdit.setStyle("-fx-text-fill: red;");
                                            return;
                                        }

                                        if (emailEdit.getText().matches("[A-Za-z0-9]+[@][A-Za-z0-9]+[.][a-z]+"))
                                        {
                                            //  pass
                                        }
                                        else
                                        {
                                            emailEdit.setStyle("-fx-text-fill: red;");
                                            return;
                                        }

                                        int N = users.size();

                                        for (int i = 0; i < N; i++)
                                        {
                                            if (loginEdit.getText().equalsIgnoreCase(users.get(i).username))
                                            {
                                                loginEdit.setStyle("-fx-text-fill: red;");
                                                return;
                                            }
                                        }

                                        loginEdit.setStyle("-fx-text-fill: black;");
                                        identificationNumberEdit.setStyle("-fx-text-fill: black;");
                                        phoneEdit.setStyle("-fx-text-fill: black;");
                                        emailEdit.setStyle("-fx-text-fill: black;");

                                        {
                                            User user = new User();
                                            user.username = loginEdit.getText();
                                            user.password = passwordEdit.getText();
                                            user.firstName = firstNameEdit.getText();
                                            user.lastName = lastNameEdit.getText();
                                            user.identificationNumber = identificationNumberEdit.getText();

                                            if (genderButton.getText().equalsIgnoreCase("Muž"))
                                                user.isMale = true;
                                            else
                                                user.isMale = false;

                                            user.phoneNumber = phoneEdit.getText();
                                            user.birthDate = birthEdit.getValue().format(DateTimeFormatter.ofPattern("dd-MM-yyyy"));
                                            user.email = emailEdit.getText();
                                            user.address = addressEdit.getText();
                                            users.add(user);

                                            try {
                                                // create a OracleDataSource instance
                                                OracleDataSource ods = new OracleDataSource();
                                                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                                                /**
                                                 * *
                                                 * To set System properties, run the Java VM with the following at
                                                 * its command line: ... -Dlogin=LOGIN_TO_ORACLE_DB
                                                 * -Dpassword=PASSWORD_TO_ORACLE_DB ... or set the project
                                                 * properties (in NetBeans: File / Project Properties / Run / VM
                                                 * Options)
                                                 */
                                                ods.setUser(databaseLogin);
                                                ods.setPassword(databasePassword);
                                                /**
                                                 *
                                                 */

                                                char gender = 'F';

                                                if (user.isMale)
                                                    gender = 'M';

                                                Timestamp ts = new Timestamp(System.currentTimeMillis());
                                                Date date = new Date();
                                                date.setTime(ts.getTime());
                                                String formattedDate = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss").format(date);

                                                String userCommand =
                                                    "INSERT INTO klient (ID_user, login, heslo, jmeno, prijmeni, pohlavi, rodne_cislo, datum_narozeni, telefon, email, adresa, begining) VALUES (" +
                                                                users.size() + ", " +
                                                                "'" + user.username + "', " +
                                                                "'" + user.password + "', " +
                                                                "'" + user.firstName + "', " +
                                                                "'" + user.lastName + "', " +
                                                                "'" + gender + "', " +
                                                                user.identificationNumber + ", " +
                                                                "'" + user.birthDate + "', " +
                                                                user.phoneNumber + ", " +
                                                                "'" + user.email + "', " +
                                                                "'" + user.address + "', " +
                                                                "TO_DATE('" + formattedDate + "', 'DD-MM-YYYY HH24:MI:SS'))";

                                                // connect to the database
                                                try (Connection conn = ods.getConnection()) {
                                                    // create a Statement
                                                    try (Statement stmt = conn.createStatement()) {
                                                        stmt.executeUpdate(userCommand);
                                                    } // close the Statement
                                                } // close the connection
                                            } catch (SQLException sqlEx) {
                                                System.err.println("SQLException: " + sqlEx.getMessage());
                                            }

                                            try
                                            {
                                                OracleDataSource ods = new OracleDataSource();
                                                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                                                ods.setUser(databaseLogin);
                                                ods.setPassword(databasePassword);

                                                try (Connection conn = ods.getConnection()) {

                                                    multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);
                                                    pictures.insertImageFromFile("src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/warning.png");
                                                }
                                            }
                                            catch (Exception ex)
                                            {
                                                System.out.println(ex.getMessage());
                                            }
                                        }

                                        handleLogin();
                                    }
                                    else
                                    {
                                        addressEdit.requestFocus();
                                    }
                                }
                                else
                                {
                                    emailEdit.requestFocus();
                                }
                            }
                            else
                            {
                                phoneEdit.requestFocus();
                            }
                        }
                        else
                        {
                            identificationNumberEdit.requestFocus();
                        }
                    }
                    else
                    {
                        lastNameEdit.requestFocus();
                    }
                }
                else
                {
                    firstNameEdit.requestFocus();
                }
            }
            else
            {
                passwordEdit.requestFocus();
            }
        }
    }

    /**
     * Open file dialog and allow user to select another picture for his account
     */
    @FXML
    private void handleImagePathButton()
    {
        if (imagePathButton.isVisible())
        {
            FileChooser fileChooser = new FileChooser();
            fileChooser.setTitle("Zvolte odpovídající soubor");

            String currentDir = System.getProperty("user.home");
            File file = new File(currentDir);
            fileChooser.setInitialDirectory(file);

            fileChooser.getExtensionFilters().addAll(new FileChooser.ExtensionFilter("Soubory obrázků", "*.png", "*.jpg", "*.gif", "*.bmp", "*.tif", "*.tiff"));

            File selectedFile = fileChooser.showOpenDialog(imagePathButton.getScene().getWindow());

            if (selectedFile != null)
            {
                String path = "file:";
                path = path + selectedFile.getPath();

                accountImage.setImage(new Image(path));

                try
                {
                    OracleDataSource ods = new OracleDataSource();
                    ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                    ods.setUser(databaseLogin);
                    ods.setPassword(databasePassword);

                    try (Connection conn = ods.getConnection()) {

                        multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);
                        pictures.updateImageFromFile(selectedFile.getPath(), loggedIn + 1);
                    }
                }
                catch (Exception ex)
                {
                    System.out.println(ex.getMessage());
                }
            }
        }
    }

    /**
     * Execute clockwise rotation of account image
     */
    @FXML
    private void handleImageRotateLeftButton()
    {
        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            String query = "{call PictureRotateLeft(?)}";

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement

                CallableStatement statement = conn.prepareCall(query);
                statement.setInt(1, loggedIn + 1);
                statement.execute();

                multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);
                accountImage.setImage(pictures.getImageFromDatabase(loggedIn + 1));
            } // close the connection
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    /**
     * Execute anti-clockwise rotation of account image
     */
    @FXML
    private void handleImageRotateRightButton()
    {
        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            String query = "{call PictureRotateRight(?)}";

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement

                CallableStatement statement = conn.prepareCall(query);
                statement.setInt(1, loggedIn + 1);
                statement.execute();

                multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);
                accountImage.setImage(pictures.getImageFromDatabase(loggedIn + 1));
            } // close the connection
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    /**
     * Execute contrast decrease of account image
     */
    @FXML
    private void handleImageContrastDownButton()
    {
        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            String query = "{call PictureMirror(?)}";

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement

                CallableStatement statement = conn.prepareCall(query);
                statement.setInt(1, loggedIn + 1);
                statement.execute();

                multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);
                accountImage.setImage(pictures.getImageFromDatabase(loggedIn + 1));
            } // close the connection
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    /**
     * Execute contrast increase of account image
     */
    @FXML
    private void handleImageContrastUpButton()
    {
        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            String query = "{call PictureContrastUp(?)}";

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement

                CallableStatement statement = conn.prepareCall(query);
                statement.setInt(1, loggedIn + 1);
                statement.execute();

                multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);
                accountImage.setImage(pictures.getImageFromDatabase(loggedIn + 1));
            } // close the connection
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    /**
     * Execute brightness decrease of account image
     */
    @FXML
    private void handleImageBrightnessDownButton()
    {
        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            String query = "{call PictureGammaDown(?)}";

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement

                CallableStatement statement = conn.prepareCall(query);
                statement.setInt(1, loggedIn + 1);
                statement.execute();

                multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);
                accountImage.setImage(pictures.getImageFromDatabase(loggedIn + 1));
            } // close the connection
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    /**
     * Execute brightness increase of account image
     */
    @FXML
    private void handleImageBrightnessUpButton()
    {
        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);

            String query = "{call PictureGammaUp(?)}";

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement

                CallableStatement statement = conn.prepareCall(query);
                statement.setInt(1, loggedIn + 1);
                statement.execute();

                multimedia.ImageIdentity pictures = new multimedia.ImageIdentity(conn);
                accountImage.setImage(pictures.getImageFromDatabase(loggedIn + 1));
            } // close the connection
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    /**
     * Move actual page to the another page by page number specified in page spinner
     * @param Page spinner object reference
     */
    @FXML
    private void handlePageChange(Object value)
    {
        if (pageChangeAllowed)
        {
            int index = (int)value;

            if (index > 0)
            {
                index--;                                        //  convert spinner value to array index

                if (actualTab == tabType.orders)
                {
                    if (index != ordersPageIndex)
                    {
                        int N = users.get(loggedIn).orders.size();

                        if ((index * 10) < N)
                        {
                            ordersPageIndex = index;
                            updateOrders();
                        }
                    }
                }
                else if (actualTab == tabType.tours)
                {
                    if (index != toursPageIndex)
                    {
                        int N = tours.size();

                        if ((index * 10) < N)
                        {
                            toursPageIndex = index;
                            updateTours();
                        }
                    }
                }
                else if (actualTab == tabType.hotels)
                {
                    if (index != hotelsPageIndex)
                    {
                        int N = hotels.size();

                        if ((index * 10) < N)
                        {
                            hotelsPageIndex = index;
                            updateHotels();
                        }
                    }
                }
                else if (actualTab == tabType.actions)
                {
                    if (index != actionsPageIndex)
                    {
                        int N = actions.size();

                        if ((index * 10) < N)
                        {
                            actionsPageIndex = index;
                            updateActions();
                        }
                    }
                }
            }
        }
    }

    /**
     * Handle selection of conrete tour from order box inside order page
     * @param Integer index of appropriate order
     * @param Integer index of appropriate tour
     */
    @FXML
    private void orderTourSelected(int orderIndex, int tourIndex)
    {
        if (orderIndex == 0)        //  first order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateOne.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).tourIndex).state);
                orderTourLocationOne.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).tourIndex).location);
                orderTourCenterOne.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).tourIndex).center);
                orderFromLabelOne.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).tourIndex).from));
                orderToLabelOne.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).tourIndex).to));
                orderHotelOne.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesOne.setText("Stravování a doprava");
                else if (bus)
                    orderServicesOne.setText("Doprava");
                else if (food)
                    orderServicesOne.setText("Stravování");
                else
                    orderServicesOne.setText("Bez služeb");

                orderMembersCountOne.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).actionsIndices.size();
                orderActionsOne.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsOne.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsOne.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 1)        //  second order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateTwo.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).tourIndex).state);
                orderTourLocationTwo.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).tourIndex).location);
                orderTourCenterTwo.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).tourIndex).center);
                orderFromLabelTwo.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).tourIndex).from));
                orderToLabelTwo.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).tourIndex).to));
                orderHotelTwo.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesTwo.setText("Stravování a doprava");
                else if (bus)
                    orderServicesTwo.setText("Doprava");
                else if (food)
                    orderServicesTwo.setText("Stravování");
                else
                    orderServicesTwo.setText("Bez služeb");

                orderMembersCountTwo.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).actionsIndices.size();
                orderActionsTwo.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsTwo.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsTwo.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 2)        //  third order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateThree.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).tourIndex).state);
                orderTourLocationThree.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).tourIndex).location);
                orderTourCenterThree.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).tourIndex).center);
                orderFromLabelThree.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).tourIndex).from));
                orderToLabelThree.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).tourIndex).to));
                orderHotelThree.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesThree.setText("Stravování a doprava");
                else if (bus)
                    orderServicesThree.setText("Doprava");
                else if (food)
                    orderServicesThree.setText("Stravování");
                else
                    orderServicesThree.setText("Bez služeb");

                orderMembersCountThree.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).actionsIndices.size();
                orderActionsThree.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsThree.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsThree.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 3)        //  fourth order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateFour.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).tourIndex).state);
                orderTourLocationFour.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).tourIndex).location);
                orderTourCenterFour.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).tourIndex).center);
                orderFromLabelFour.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).tourIndex).from));
                orderToLabelFour.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).tourIndex).to));
                orderHotelFour.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesFour.setText("Stravování a doprava");
                else if (bus)
                    orderServicesFour.setText("Doprava");
                else if (food)
                    orderServicesFour.setText("Stravování");
                else
                    orderServicesFour.setText("Bez služeb");

                orderMembersCountFour.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).actionsIndices.size();
                orderActionsFour.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsFour.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsFour.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 4)        //  fifth order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateFive.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).tourIndex).state);
                orderTourLocationFive.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).tourIndex).location);
                orderTourCenterFive.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).tourIndex).center);
                orderFromLabelFive.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).tourIndex).from));
                orderToLabelFive.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).tourIndex).to));
                orderHotelFive.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesFive.setText("Stravování a doprava");
                else if (bus)
                    orderServicesFive.setText("Doprava");
                else if (food)
                    orderServicesFive.setText("Stravování");
                else
                    orderServicesFive.setText("Bez služeb");

                orderMembersCountFive.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).actionsIndices.size();
                orderActionsFive.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsFive.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsFive.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 5)        //  sixth order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateSix.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).tourIndex).state);
                orderTourLocationSix.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).tourIndex).location);
                orderTourCenterSix.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).tourIndex).center);
                orderFromLabelSix.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).tourIndex).from));
                orderToLabelSix.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).tourIndex).to));
                orderHotelSix.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesSix.setText("Stravování a doprava");
                else if (bus)
                    orderServicesSix.setText("Doprava");
                else if (food)
                    orderServicesSix.setText("Stravování");
                else
                    orderServicesSix.setText("Bez služeb");

                orderMembersCountSix.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).actionsIndices.size();
                orderActionsSix.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsSix.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsSix.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 6)        //  seventh order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateSeven.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).tourIndex).state);
                orderTourLocationSeven.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).tourIndex).location);
                orderTourCenterSeven.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).tourIndex).center);
                orderFromLabelSeven.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).tourIndex).from));
                orderToLabelSeven.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).tourIndex).to));
                orderHotelSeven.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesSeven.setText("Stravování a doprava");
                else if (bus)
                    orderServicesSeven.setText("Doprava");
                else if (food)
                    orderServicesSeven.setText("Stravování");
                else
                    orderServicesSeven.setText("Bez služeb");

                orderMembersCountSeven.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).actionsIndices.size();
                orderActionsSeven.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsSeven.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsSeven.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 7)        //  eighth order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateEight.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).tourIndex).state);
                orderTourLocationEight.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).tourIndex).location);
                orderTourCenterEight.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).tourIndex).center);
                orderFromLabelEight.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).tourIndex).from));
                orderToLabelEight.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).tourIndex).to));
                orderHotelEight.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesEight.setText("Stravování a doprava");
                else if (bus)
                    orderServicesEight.setText("Doprava");
                else if (food)
                    orderServicesEight.setText("Stravování");
                else
                    orderServicesEight.setText("Bez služeb");

                orderMembersCountEight.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).actionsIndices.size();
                orderActionsEight.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsEight.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsEight.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 8)        //  ninth order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateNine.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).tourIndex).state);
                orderTourLocationNine.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).tourIndex).location);
                orderTourCenterNine.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).tourIndex).center);
                orderFromLabelNine.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).tourIndex).from));
                orderToLabelNine.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).tourIndex).to));
                orderHotelNine.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesNine.setText("Stravování a doprava");
                else if (bus)
                    orderServicesNine.setText("Doprava");
                else if (food)
                    orderServicesNine.setText("Stravování");
                else
                    orderServicesNine.setText("Bez služeb");

                orderMembersCountNine.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).actionsIndices.size();
                orderActionsNine.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsNine.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsNine.getSelectionModel().select(0);
            }
        }
        else if (orderIndex == 9)        //  tenth order box
        {
            if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.size() > tourIndex && tourIndex >= 0)
            {
                orderTourStateTen.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).tourIndex).state);
                orderTourLocationTen.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).tourIndex).location);
                orderTourCenterTen.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).tourIndex).center);
                orderFromLabelTen.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).tourIndex).from));
                orderToLabelTen.setText(RichString.toRealDate(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).tourIndex).to));
                orderHotelTen.setText(toursRestore.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).tourIndex).hotel.name);

                boolean food = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).food;
                boolean bus = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).bus;

                if (bus && food)
                    orderServicesTen.setText("Stravování a doprava");
                else if (bus)
                    orderServicesTen.setText("Doprava");
                else if (food)
                    orderServicesTen.setText("Stravování");
                else
                    orderServicesTen.setText("Bez služeb");

                orderMembersCountTen.setText("Počet osob: " + users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).personCount);

                int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).actionsIndices.size();
                orderActionsTen.getItems().clear();

                for (int i = 0; i < N; i++)
                    orderActionsTen.getItems().add(actions.get(users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).orders.get(tourIndex).actionsIndices.get(i)).name);

                orderActionsTen.getSelectionModel().select(0);
            }
        }
    }

    /**
     * Handle selection of concrete tour from tours page
     * @param Integer index of appropriate tour
     */
    @FXML
    private void handleTourPick(int index)
    {
        if (loggedIn >= 0)
        {
            orderTourProcedure = toursPageIndex * 10 + index;
            hotels.clear();
            int N = toursRestore.size();

            for (int i = 0; i < N; i++)
            {
                if (tours.get(orderTourProcedure).state.equalsIgnoreCase(toursRestore.get(i).state) &&
                    tours.get(orderTourProcedure).location.equalsIgnoreCase(toursRestore.get(i).location) &&
                    tours.get(orderTourProcedure).center.equalsIgnoreCase(toursRestore.get(i).center) &&
                    tours.get(orderTourProcedure).from.equalsIgnoreCase(toursRestore.get(i).from) &&
                    tours.get(orderTourProcedure).to.equalsIgnoreCase(toursRestore.get(i).to))
                {
                    hotels.add(toursRestore.get(i).hotel);
                }
            }

            hotelsPageIndex = 0;
            hotelsScrollPane.setVvalue(0.0);
            updateHotels();

            clientTab.setDisable(true);
            ordersTab.setDisable(true);
            toursTab.setDisable(true);
            actionsTab.setDisable(true);

            actualTab = tabType.hotels;
            tabs.getSelectionModel().select(3);
        }
    }

    /**
     * Handle selection of concrete hotel from hotels page
     * @param Integer index of appropriate hotel
     */
    @FXML
    private void handleHotelPick(int index)
    {
        if (loggedIn >= 0 && orderTourProcedure >= 0)
        {
            actionsTab.setDisable(false);
            hotelsTab.setDisable(true);

            actualTab = tabType.actions;
            tabs.getSelectionModel().select(4);
            orderHotelProcedure = hotelsPageIndex * 10 + index;

            setPersonSpinnerVisible(true);
        }
    }

    /**
     * Handle acception of new order
     */
    @FXML
    private void handleOrderPick()
    {
        if (loggedIn >= 0 && orderTourProcedure >= 0 && orderHotelProcedure >= 0)
        {
            setPersonSpinnerVisible(false);

            clientTab.setDisable(false);
            ordersTab.setDisable(false);
            toursTab.setDisable(false);
            hotelsTab.setDisable(false);
            actionsTab.setDisable(false);

            actualTab = tabType.tours;
            tabs.getSelectionModel().select(2);

            Order order = new Order();
            order.personCount = (int)personSpinner.getValue();
            order.tourIndex = 0;

            int N = toursRestore.size();

            for (int i = 0; i < N; i++)
            {
                if (toursRestore.get(i).state.equalsIgnoreCase(tours.get(orderTourProcedure).state) &&
                    toursRestore.get(i).location.equalsIgnoreCase(tours.get(orderTourProcedure).location) &&
                    toursRestore.get(i).center.equalsIgnoreCase(tours.get(orderTourProcedure).center) &&
                    toursRestore.get(i).from.equalsIgnoreCase(tours.get(orderTourProcedure).from) &&
                    toursRestore.get(i).to.equalsIgnoreCase(tours.get(orderTourProcedure).to) &&
                    toursRestore.get(i).hotel.name.equalsIgnoreCase(hotels.get(orderHotelProcedure).name) &&
                    toursRestore.get(i).hotel.stars == hotels.get(orderHotelProcedure).stars)
                {
                    order.tourIndex = i;
                    order.food = toursRestore.get(i).food;
                    order.bus = toursRestore.get(i).bus;
                    break;
                }
            }

            N = actions.size();

            for (int i = 0; i < N; i++)
            {
                if (actions.get(i).want)
                    order.actionsIndices.add(i);
            }

            hotels.clear();
            N = toursRestore.size();

            for (int i = 0; i < N; i++)
                hotels.add(hotelsRestore.get(i));

            hotelsPageIndex = 0;
            hotelsScrollPane.setVvalue(0.0);
            updateHotels();

            boolean isNewRequired = false;

            if (users.get(loggedIn).orders.size() > 0)
            {
                if (users.get(loggedIn).orders.get(users.get(loggedIn).orders.size() - 1).accepted)
                    isNewRequired = true;
            }
            else
                isNewRequired = true;

            if (isNewRequired)
            {
                OrderPack orderPack = new OrderPack();
                orderPack.orderDate = new SimpleDateFormat("dd-MM-yyyy").format(new Date());
                users.get(loggedIn).orders.add(orderPack);
            }

            users.get(loggedIn).orders.get(users.get(loggedIn).orders.size() - 1).orders.add(order);

            orderTourProcedure = -1;
            orderHotelProcedure = -1;

            updateOrders();
        }
    }

    /**
     * Handle acception or rejection of concrete order inside orders page
     * @param Integer index of concrete order
     */
    @FXML
    private void handleOrderAccept(int index)
    {
        if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).accepted)
        {
            users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).cancelled = true;

            List<Integer> indices = new ArrayList<Integer>();

            int userID = -1;

            try {
                // create a OracleDataSource instance
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                /**
                 * *
                 * To set System properties, run the Java VM with the following at
                 * its command line: ... -Dlogin=LOGIN_TO_ORACLE_DB
                 * -Dpassword=PASSWORD_TO_ORACLE_DB ... or set the project
                 * properties (in NetBeans: File / Project Properties / Run / VM
                 * Options)
                 */
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);
                /**
                 *
                 */
                // connect to the database
                try (Connection conn = ods.getConnection()) {
                    // create a Statement
                    try (Statement stmt = conn.createStatement()) {

                        String command = "SELECT ID_user FROM klient WHERE login = '" + users.get(loggedIn).username + "'";

                        // select something from the system's dual table
                        try (ResultSet rset = stmt.executeQuery(command)) {
                            // iterate through the result and print the values
                            while (rset.next()) {
                                userID = Integer.parseInt(rset.getObject(1).toString());
                            }
                        } // close the ResultSet
                    } // close the Statement
                } // close the connection

            } catch (SQLException sqlEx) {
                System.err.println("SQLException: " + sqlEx.getMessage());
            }

            try {
                // create a OracleDataSource instance
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                /**
                 * *
                 * To set System properties, run the Java VM with the following at
                 * its command line: ... -Dlogin=LOGIN_TO_ORACLE_DB
                 * -Dpassword=PASSWORD_TO_ORACLE_DB ... or set the project
                 * properties (in NetBeans: File / Project Properties / Run / VM
                 * Options)
                 */
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);
                /**
                 *
                 */
                // connect to the database
                try (Connection conn = ods.getConnection()) {
                    // create a Statement
                    try (Statement stmt = conn.createStatement()) {

                        String command = "SELECT ID_objednavky FROM objednavka_uzivatel WHERE ID_user = " + userID;

                        // select something from the system's dual table
                        try (ResultSet rset = stmt.executeQuery(command)) {
                            // iterate through the result and print the values
                            while (rset.next()) {
                                int value = Integer.parseInt(rset.getObject(1).toString());
                                indices.add(value);
                            }
                        } // close the ResultSet
                    } // close the Statement
                } // close the connection

            } catch (SQLException sqlEx) {
                System.err.println("SQLException: " + sqlEx.getMessage());
            }

            int databaseIndex = indices.get(ordersPageIndex * 10 + index);

            try {
                // create a OracleDataSource instance
                OracleDataSource ods = new OracleDataSource();
                ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                ods.setUser(databaseLogin);
                ods.setPassword(databasePassword);

                String command = "UPDATE objednavka SET " + "zrusena = 'Y'" + " WHERE ID_objednavky = " + databaseIndex;

                // connect to the database
                try (Connection conn = ods.getConnection()) {
                    // create a Statement
                    try (Statement stmt = conn.createStatement()) {
                        stmt.executeUpdate(command);
                    } // close the Statement
                } // close the connection

                command = "CALL DELETE_TMP('objednavka', 'ID_objednavky', " + databaseIndex + ")";
                try (Connection conn = ods.getConnection()) {
                    // create a Statement
                    try (Statement stmt = conn.createStatement()) {
                        stmt.executeUpdate(command);
                    } // close the Statement
                } // close the connection
            } catch (SQLException sqlEx) {
                System.err.println("SQLException: " + sqlEx.getMessage());
            }

            if (index == 0)
            {
                orderAcceptOne.setVisible(false);
                orderAcceptOne.setManaged(false);

                orderImageOne.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 1)
            {
                orderAcceptTwo.setVisible(false);
                orderAcceptTwo.setManaged(false);

                orderImageTwo.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 2)
            {
                orderAcceptThree.setVisible(false);
                orderAcceptThree.setManaged(false);

                orderImageThree.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 3)
            {
                orderAcceptFour.setVisible(false);
                orderAcceptFour.setManaged(false);

                orderImageFour.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 4)
            {
                orderAcceptFive.setVisible(false);
                orderAcceptFive.setManaged(false);

                orderImageFive.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 5)
            {
                orderAcceptSix.setVisible(false);
                orderAcceptSix.setManaged(false);

                orderImageSix.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 6)
            {
                orderAcceptSeven.setVisible(false);
                orderAcceptSeven.setManaged(false);

                orderImageSeven.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 7)
            {
                orderAcceptEight.setVisible(false);
                orderAcceptEight.setManaged(false);

                orderImageEight.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 8)
            {
                orderAcceptNine.setVisible(false);
                orderAcceptNine.setManaged(false);

                orderImageNine.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
            else if (index == 9)
            {
                orderAcceptTen.setVisible(false);
                orderAcceptTen.setManaged(false);

                orderImageTen.setImage(new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/cancel.png"));
            }
        }
        else
        {
            if (loggedIn >= 0)
            {
                if (index == 0)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 0).accepted = true;

                    orderAcceptOne.setText("Zrušit");
                    orderAcceptOne.setVisible(true);
                    orderAcceptOne.setManaged(true);
                }
                else if (index == 1)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 1).accepted = true;

                    orderAcceptTwo.setText("Zrušit");
                    orderAcceptTwo.setVisible(true);
                    orderAcceptTwo.setManaged(true);
                }
                else if (index == 2)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 2).accepted = true;

                    orderAcceptThree.setText("Zrušit");
                    orderAcceptThree.setVisible(true);
                    orderAcceptThree.setManaged(true);
                }
                else if (index == 3)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 3).accepted = true;

                    orderAcceptFour.setText("Zrušit");
                    orderAcceptFour.setVisible(true);
                    orderAcceptFour.setManaged(true);
                }
                else if (index == 4)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 4).accepted = true;

                    orderAcceptFive.setText("Zrušit");
                    orderAcceptFive.setVisible(true);
                    orderAcceptFive.setManaged(true);
                }
                else if (index == 5)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 5).accepted = true;

                    orderAcceptSix.setText("Zrušit");
                    orderAcceptSix.setVisible(true);
                    orderAcceptSix.setManaged(true);
                }
                else if (index == 6)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 6).accepted = true;

                    orderAcceptSeven.setText("Zrušit");
                    orderAcceptSeven.setVisible(true);
                    orderAcceptSeven.setManaged(true);
                }
                else if (index == 7)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 7).accepted = true;

                    orderAcceptEight.setText("Zrušit");
                    orderAcceptEight.setVisible(true);
                    orderAcceptEight.setManaged(true);
                }
                else if (index == 8)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 8).accepted = true;

                    orderAcceptNine.setText("Zrušit");
                    orderAcceptNine.setVisible(true);
                    orderAcceptNine.setManaged(true);
                }
                else if (index == 9)
                {
                    users.get(loggedIn).orders.get(ordersPageIndex * 10 + 9).accepted = true;

                    orderAcceptTen.setText("Zrušit");
                    orderAcceptTen.setVisible(true);
                    orderAcceptTen.setManaged(true);
                }

                try {
                    // create a OracleDataSource instance
                    OracleDataSource ods = new OracleDataSource();
                    ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                    ods.setUser(databaseLogin);
                    ods.setPassword(databasePassword);

                    Timestamp ts = new Timestamp(System.currentTimeMillis());
                    Date date = new Date();
                    date.setTime(ts.getTime());
                    String formattedDate = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss").format(date);

                    ordersCount++;

                    String orderCommand = "INSERT INTO objednavka (ID_objednavky, zrusena, termin, begining) VALUES (" +
                            ordersCount + ", " +
                            "'N', '" +
                            users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).orderDate + "', TO_DATE('" + formattedDate + "', 'DD-MM-YYYY HH24:MI:SS'))";

                    // connect to the database
                    try (Connection conn = ods.getConnection()) {
                        // create a Statement
                        try (Statement stmt = conn.createStatement()) {
                            stmt.executeUpdate(orderCommand);
                        } // close the Statement
                    } // close the connection

                    orderCommand = "INSERT INTO objednavka_uzivatel (ID_objednavka_uzivatel, ID_user, ID_objednavky, begining) VALUES (" +
                            (users.get(loggedIn).orders.size() + 1) + ", " +
                            (loggedIn + 1) + ", " +
                            ordersCount + ", TO_DATE('" + formattedDate + "', 'DD-MM-YYYY HH24:MI:SS'))";

                    // connect to the database
                    try (Connection conn = ods.getConnection()) {
                        // create a Statement
                        try (Statement stmt = conn.createStatement()) {
                            stmt.executeUpdate(orderCommand);
                        } // close the Statement
                    } // close the connection

                    int M = users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).orders.size();

                    for (int i = 0; i < M; i++)
                    {
                        char food = 'N';
                        char bus = 'N';

                        if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).orders.get(i).food)
                            food = 'Y';

                        if (users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).orders.get(i).bus)
                            bus = 'Y';

                        orderToursCount++;

                        String orderTourCommand = "INSERT INTO objednavka_zajezdu (ID_objednavky_zajezdu, ID_objednavky, ID_zajezdu, strava, doprava, pocet_osob, begining) VALUES (" +
                                orderToursCount + ", " +
                                ordersCount + ", " +
                                (users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).orders.get(i).tourIndex + 1) + ", " +
                                "'" + food + "', " +
                                "'" + bus + "', " +
                                users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).orders.get(i).personCount + ", TO_DATE('" + formattedDate + "', 'DD-MM-YYYY HH24:MI:SS'))";

                        // connect to the database
                        try (Connection conn = ods.getConnection()) {
                            // create a Statement
                            try (Statement stmt = conn.createStatement()) {
                                stmt.executeUpdate(orderTourCommand);
                            } // close the Statement
                        } // close the connection

                        int N = users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).orders.get(i).actionsIndices.size();

                        for (int j = 0; j < N; j++)
                        {
                            orderActionsCount++;

                            String orderActionCommand = "INSERT INTO objednavka_doprovodne_akce (ID_objednavky_doprovodne_akce, ID_objednavky_zajezdu, ID_doprovodne_akce, begining) VALUES (" +
                                    orderActionsCount + ", " +
                                    orderToursCount + ", " +
                                    (users.get(loggedIn).orders.get(ordersPageIndex * 10 + index).orders.get(i).actionsIndices.get(j) + 1) + ", TO_DATE('" + formattedDate + "', 'DD-MM-YYYY HH24:MI:SS'))";

                            // connect to the database
                            try (Connection conn = ods.getConnection()) {
                                // create a Statement
                                try (Statement stmt = conn.createStatement()) {
                                    stmt.executeUpdate(orderActionCommand);
                                } // close the Statement
                            } // close the connection
                        }
                    }
                } catch (SQLException sqlEx) {
                    System.err.println("SQLException: " + sqlEx.getMessage());
                }
            }
        }
    }

    /**
     * Toggle visibility of person spinner element
     * @param True or false value which represents visibility of element
     */
    @FXML
    private void setPersonSpinnerVisible(boolean value)
    {
        if (value)
        {
            if (personSpinner.isVisible() == false)
            {
                insertButton.setVisible(true);
                insertButton.setManaged(true);

                personSpinner.setVisible(true);
                personSpinner.setManaged(true);
            }
        }
        else
        {
            if (personSpinner.isVisible())
            {
                insertButton.setVisible(false);
                insertButton.setManaged(false);

                personSpinner.setVisible(false);
                personSpinner.setManaged(false);
            }
        }
    }

    /**
     * Call this method every time when tour filter has been applied
     */
    @FXML
    private void handleFilter()
    {
        if (similarityActive)
            return;

        tours.clear();
        int M = toursRestore.size();

        for (int i = 0; i < M; i++)
        {
            boolean found = false;
            int N = tours.size();

            for (int j = 0; j < N; j++)
            {
                if (tours.get(j).state.equalsIgnoreCase(toursRestore.get(i).state) && tours.get(j).location.equalsIgnoreCase(toursRestore.get(i).location) &&
                    tours.get(j).center.equalsIgnoreCase(toursRestore.get(i).center) && tours.get(j).from.equalsIgnoreCase(toursRestore.get(i).from) &&
                    tours.get(j).to.equalsIgnoreCase(toursRestore.get(i).to))
                {
                    found = true;
                    break;
                }
            }

            if (found == false)
                tours.add(toursRestore.get(i));
        }

        String state = "";
        String location = "";
        String center = "";
        String from = "";
        String to = "";

        state = filterState.getText();
        location = filterLocation.getText();
        center = filterCenter.getText();

        if (filterFrom.getValue() != null)
            from = filterFrom.getValue().format(DateTimeFormatter.ofPattern("dd-MM-yyyy"));

        if (filterTo.getValue() != null)
            to = filterTo.getValue().format(DateTimeFormatter.ofPattern("dd-MM-yyyy"));

        if (state.length() > 0)
        {
            state = state.toLowerCase();

            List<Tour> tempTours = new ArrayList<Tour>();

            int N = tours.size();

            for (int i = 0; i < N; i++)
            {
                tempTours.add(tours.get(i));
            }

            tours.clear();

            for (int i = 0; i < N; i++)
            {
                String actualState = tempTours.get(i).state.toLowerCase();

                if (actualState.contains(state))
                {
                    tours.add(tempTours.get(i));
                }
            }
        }

        if (location.length() > 0)
        {
            location = location.toLowerCase();

            List<Tour> tempTours = new ArrayList<Tour>();

            int N = tours.size();

            for (int i = 0; i < N; i++)
            {
                tempTours.add(tours.get(i));
            }

            tours.clear();

            for (int i = 0; i < N; i++)
            {
                String actualLocation = tempTours.get(i).location.toLowerCase();

                if (actualLocation.contains(location))
                {
                    tours.add(tempTours.get(i));
                }
            }
        }

        if (center.length() > 0)
        {
            center = center.toLowerCase();

            List<Tour> tempTours = new ArrayList<Tour>();

            int N = tours.size();

            for (int i = 0; i < N; i++)
            {
                tempTours.add(tours.get(i));
            }

            tours.clear();

            for (int i = 0; i < N; i++)
            {
                String actualCenter = tempTours.get(i).center.toLowerCase();

                if (actualCenter.contains(center))
                {
                    tours.add(tempTours.get(i));
                }
            }
        }

        if (from.length() > 0)
        {
            List<Tour> tempTours = new ArrayList<Tour>();

            int N = tours.size();

            for (int i = 0; i < N; i++)
            {
                tempTours.add(tours.get(i));
            }

            tours.clear();

            SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy");

            for (int i = 0; i < N; i++)
            {
                Date first;
                Date second;

                try
                {
                    first = sdf.parse(from);
                    second = sdf.parse(tempTours.get(i).from);

                    if (first.before(second))
                        tours.add(tempTours.get(i));
                }
                catch(ParseException ex)
                {
                    //  pass
                }
            }
        }

        if (to.length() > 0)
        {
            List<Tour> tempTours = new ArrayList<Tour>();

            int N = tours.size();

            for (int i = 0; i < N; i++)
            {
                tempTours.add(tours.get(i));
            }

            tours.clear();

            SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy");

            for (int i = 0; i < N; i++)
            {
                Date first;
                Date second;

                try
                {
                    first = sdf.parse(tempTours.get(i).to);
                    second = sdf.parse(to);

                    if (first.before(second))
                        tours.add(tempTours.get(i));
                }
                catch(ParseException ex)
                {
                    //  pass
                }
            }
        }

        toursPageIndex = 0;

        actualTab = tabType.tours;
        int N = tours.size();

        pageChangeAllowed = false;
        int oldIndex = toursPageIndex;
        pageSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, N / 10 + 1));
        pageSpinner.getValueFactory().setValue(oldIndex + 1);
        pageChangeAllowed = true;

        updateTours();
    }

    /**
     * Apply similarity filter which contains searching of most similar tours
     */
    @FXML
    private void handleSimilarity()
    {
        if (similarityActive)
        {
            toursPageIndex = 0;

            actualTab = tabType.tours;
            int N = tours.size();

            pageChangeAllowed = false;
            int oldIndex = toursPageIndex;
            pageSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, N / 10 + 1));
            pageSpinner.getValueFactory().setValue(oldIndex + 1);
            pageChangeAllowed = true;

            initTours();

            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/new_tab.png");
            similarityButton.setGraphic(new ImageView(image));

            similarityActive = false;
        }
        else
        {
            FileChooser fileChooser = new FileChooser();
            fileChooser.setTitle("Zvolte odpovídající soubor");

            String currentDir = System.getProperty("user.home");
            File file = new File(currentDir);
            fileChooser.setInitialDirectory(file);

            fileChooser.getExtensionFilters().addAll(new FileChooser.ExtensionFilter("Soubory obrázků", "*.png", "*.jpg", "*.gif", "*.bmp", "*.tif", "*.tiff"));

            File selectedFile = fileChooser.showOpenDialog(imagePathButton.getScene().getWindow());

            if (selectedFile != null)
            {
                try
                {
                    OracleDataSource ods = new OracleDataSource();
                    ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
                    ods.setUser(databaseLogin);
                    ods.setPassword(databasePassword);

                    try (Connection conn = ods.getConnection()) {

                        multimedia.ImageTour pictures = new multimedia.ImageTour(conn);
                        pictures.insertImageFromFile(selectedFile.getPath());
                        List<Integer> indices = pictures.similarity(pictures.getMaxId());
                        pictures.deleteImageById(pictures.getMaxId());

                        tours.clear();
                        int M = indices.size();

                        for (int i = 0; i < M; i++)
                        {
                            int k = indices.get(i) - 1;
                            int N = tours.size();
                            boolean found = false;

                            for (int j = 0; j < N; j++)
                            {
                                if (tours.get(j).state.equalsIgnoreCase(toursRestore.get(k).state) && tours.get(j).location.equalsIgnoreCase(toursRestore.get(k).location) &&
                                    tours.get(j).center.equalsIgnoreCase(toursRestore.get(k).center) && tours.get(j).from.equalsIgnoreCase(toursRestore.get(k).from) &&
                                    tours.get(j).to.equalsIgnoreCase(toursRestore.get(k).to))
                                {
                                    found = true;
                                    break;
                                }
                            }

                            if (found == false)
                                tours.add(toursRestore.get(k));
                        }

                        while (tours.size() > 5)
                            tours.remove(tours.size() - 1);

                        toursPageIndex = 0;

                        actualTab = tabType.tours;
                        int N = tours.size();

                        pageChangeAllowed = false;
                        int oldIndex = toursPageIndex;
                        pageSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, N / 10 + 1));
                        pageSpinner.getValueFactory().setValue(oldIndex + 1);
                        pageChangeAllowed = true;

                        updateTours();

                        Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/close.png");
                        similarityButton.setGraphic(new ImageView(image));

                        similarityActive = true;
                    }
                }
                catch (Exception ex)
                {
                    System.out.println(ex.getMessage());
                }
            }
        }
    }

    /**
     * Toggle visibility of filters tray
     * @param Boolean value which represents visibility of tray
     */
    @FXML
    private void setFiltersVisible(boolean value)
    {
        if (value)
        {
            if (filterState.isVisible() == false)
            {
                filterState.setVisible(true);
                filterState.setManaged(true);

                filterLocation.setVisible(true);
                filterLocation.setManaged(true);

                filterCenter.setVisible(true);
                filterCenter.setManaged(true);

                filterFrom.setVisible(true);
                filterFrom.setManaged(true);

                filterTo.setVisible(true);
                filterTo.setManaged(true);

                similarityButton.setVisible(true);
                similarityButton.setManaged(true);
            }
        }
        else
        {
            if (filterState.isVisible())
            {
                filterState.setVisible(false);
                filterState.setManaged(false);

                filterLocation.setVisible(false);
                filterLocation.setManaged(false);

                filterCenter.setVisible(false);
                filterCenter.setManaged(false);

                filterFrom.setVisible(false);
                filterFrom.setManaged(false);

                filterTo.setVisible(false);
                filterTo.setManaged(false);

                similarityButton.setVisible(false);
                similarityButton.setManaged(false);
            }
        }
    }

    /**
     * Toggle visibility of pafe spinner
     * @param Boolean value which represents visibility of spinner
     */
    @FXML
    private void setPageSpinnerVisible(boolean value)
    {
        if (value)
        {
            if (pageSpinner.isVisible() == false)
            {
                pageSpinner.setVisible(true);
                pageSpinner.setManaged(true);
            }
        }
        else
        {
            if (pageSpinner.isVisible())
            {
                pageSpinner.setVisible(false);
                pageSpinner.setManaged(false);
            }
        }
    }

    /**
     * Initialize all spinners and setup them to default states
     */
    @FXML
    private void initTray()
    {
        personSpinner.getStyleClass().add(personSpinner.STYLE_CLASS_ARROWS_ON_RIGHT_HORIZONTAL);
        personSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, 100));
        personSpinner.getValueFactory().setValue(2);
        setPersonSpinnerVisible(false);

        pageSpinner.getStyleClass().add(pageSpinner.STYLE_CLASS_ARROWS_ON_RIGHT_HORIZONTAL);
        pageSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, 10));
        pageSpinner.getValueFactory().setValue(1);
        setPageSpinnerVisible(false);
        setFiltersVisible(false);
    }

    /**
     * Apply all visual effects using appropriate CSS commands
     */
    @FXML
    private void applyEffects()
    {
        account.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");

        {
            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/folder.png");
            imagePathButton.setGraphic(new ImageView(image));
        }

        {
            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/rotateRight.png");
            imageRotateLeftButton.setGraphic(new ImageView(image));
        }

        {
            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/rotateLeft.png");
            imageRotateRightButton.setGraphic(new ImageView(image));
        }

        {
            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/mirror.png");
            imageContrastDownButton.setGraphic(new ImageView(image));
        }

        {
            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/redo.png");
            imageContrastUpButton.setGraphic(new ImageView(image));
        }

        {
            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/down.png");
            imageBrightnessDownButton.setGraphic(new ImageView(image));
        }

        {
            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/up.png");
            imageBrightnessUpButton.setGraphic(new ImageView(image));
        }

        tourOne.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourTwo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourThree.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourFour.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourFive.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourSix.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourSeven.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourEight.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourNine.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        tourTen.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");

        stateLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        stateLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        locationLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        centerLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        fromLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        toLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        hotelOne.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelTwo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelThree.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelFour.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelFive.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelSix.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelSeven.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelEight.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelNine.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        hotelTen.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");

        hotelLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        hotelLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");

        actionOne.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionTwo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionThree.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionFour.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionFive.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionSix.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionSeven.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionEight.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionNine.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        actionTen.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");

        actionLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        actionLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        personsLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        actionFromLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        actionToLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");

        orderOne.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderTwo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderThree.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderFour.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderFive.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderSix.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderSeven.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderEight.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderNine.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");
        orderTen.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.8), 50, 0, 0, 0);");

        orderDateOne.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesOne.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountOne.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountTwo.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateThree.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesThree.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountThree.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateFour.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesFour.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountFour.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateFive.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesFive.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountFive.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateSix.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesSix.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountSix.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountSeven.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateEight.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesEight.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountEight.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateNine.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesNine.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountNine.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderDateTen.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(255, 150, 0, 255);");
        orderTourStateTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 16px;" +
                "-fx-text-fill: rgba(50, 50, 50, 255);");
        orderTourLocationTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderTourCenterTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderFromLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: green;");
        orderToLabelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(200, 0, 40, 255);");
        orderHotelTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 15px;" +
                "-fx-text-fill: rgba(75, 75, 75, 255);");
        orderServicesTen.setStyle("-fx-font-weight: bold;" +
                "-fx-font-size: 14px;" +
                "-fx-text-fill: rgba(100, 100, 100, 255);");
        orderMembersCountTen.setStyle("-fx-font-weight: bold;" +
                "-fx-text-fill: rgba(0, 100, 160, 255);");

        orderSeparatorOne.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        orderSeparatorTwo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        orderSeparatorThree.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        orderSeparatorFour.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        orderSeparatorFive.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        orderSeparatorSix.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        orderSeparatorSeven.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        orderSeparatorEight.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        orderSeparatorNine.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");

        tourSeparatorOne.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        tourSeparatorTwo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        tourSeparatorThree.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        tourSeparatorFour.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        tourSeparatorFive.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        tourSeparatorSix.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        tourSeparatorSeven.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        tourSeparatorEight.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        tourSeparatorNine.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");

        hotelSeparatorOne.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        hotelSeparatorTwo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        hotelSeparatorThree.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        hotelSeparatorFour.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        hotelSeparatorFive.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        hotelSeparatorSix.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        hotelSeparatorSeven.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        hotelSeparatorEight.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        hotelSeparatorNine.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");

        actionSeparatorOne.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        actionSeparatorTwo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        actionSeparatorThree.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        actionSeparatorFour.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        actionSeparatorFive.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        actionSeparatorSix.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        actionSeparatorSeven.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        actionSeparatorEight.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");
        actionSeparatorNine.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,1.0), 50, 0, 0, 0);");

        filterState.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");
        filterLocation.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");
        filterCenter.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");
        filterFrom.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");
        filterTo.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");
        personSpinner.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");
        insertButton.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");
        pageSpinner.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");

        {
            Image image = new Image("file:src/main/java/cz/vutbr/fit/pdb/project01/sample/resources/new_tab.png");
            similarityButton.setGraphic(new ImageView(image));
            similarityButton.setStyle("-fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.4), 10, 0, 0, 0);");
        }
    }

    /**
     * Load all required images and data objects into to client from remote database
     */
    @FXML
    private void initFromDatabase()
    {
        List<ConceptUser> conceptUsers = new ArrayList<ConceptUser>();
        List<ConceptHotel> conceptHotels = new ArrayList<ConceptHotel>();
        List<ConceptAction> conceptActions = new ArrayList<ConceptAction>();
        List<ConceptTour> conceptTours = new ArrayList<ConceptTour>();
        List<ConceptOrder> conceptOrders = new ArrayList<ConceptOrder>();
        List<ConceptOrderUser> conceptOrderUsers = new ArrayList<ConceptOrderUser>();
        List<ConceptOrderTour> conceptOrderTours = new ArrayList<ConceptOrderTour>();
        List<ConceptOrderAction> conceptOrderActions = new ArrayList<ConceptOrderAction>();

        try {
            // create a OracleDataSource instance
            OracleDataSource ods = new OracleDataSource();
            ods.setURL("jdbc:oracle:thin:@//gort.fit.vutbr.cz:1521/orclpdb.gort.fit.vutbr.cz");
            /**
             * *
             * To set System properties, run the Java VM with the following at
             * its command line: ... -Dlogin=LOGIN_TO_ORACLE_DB
             * -Dpassword=PASSWORD_TO_ORACLE_DB ... or set the project
             * properties (in NetBeans: File / Project Properties / Run / VM
             * Options)
             */
            ods.setUser(databaseLogin);
            ods.setPassword(databasePassword);
            /**
             *
             */
            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {
                    // select something from the system's dual table
                    try (ResultSet rset = stmt.executeQuery(
                            "SELECT * FROM klient")) {
                        // iterate through the result and print the values
                        while (rset.next()) {

                            databaseLoads++;

                            ConceptUser user = new ConceptUser();
                            user.login = rset.getObject(1).toString();
                            user.password = rset.getObject(2).toString();
                            user.firstName = rset.getObject(3).toString();
                            user.lastName = rset.getObject(4).toString();

                            if (rset.getObject(5).toString().equalsIgnoreCase("M"))
                                user.isMale = true;
                            else
                                user.isMale = false;

                            user.identificationNumber = rset.getObject(6).toString();
                            user.birthDate = rset.getObject(7).toString();
                            user.phone = rset.getObject(8).toString();
                            user.email = rset.getObject(9).toString();
                            user.address = rset.getObject(10).toString();
//                            user.ID_user = Integer.parseInt(rset.getObject(11).toString());
//                            user.begining = rset.getObject(12).toString();
//                            user.ending = rset.getObject(13).toString();
                            conceptUsers.add(user);
                        }
                    } // close the ResultSet
                } // close the Statement
            } // close the connection

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {
                    // select something from the system's dual table
                    try (ResultSet rset = stmt.executeQuery(
                            "SELECT * FROM hotel")) {
                        // iterate through the result and print the values
                        while (rset.next()) {

                            databaseLoads++;

                            ConceptHotel hotel = new ConceptHotel();
                            hotel.ID_hotel = Integer.parseInt(rset.getObject(1).toString());
                            hotel.name = rset.getObject(2).toString();
                            hotel.stars = Integer.parseInt(rset.getObject(3).toString());
                            conceptHotels.add(hotel);
                        }
                    } // close the ResultSet
                } // close the Statement
            } // close the connection

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {
                    // select something from the system's dual table
                    try (ResultSet rset = stmt.executeQuery(
                            "SELECT * FROM doprovodna_akce")) {
                        // iterate through the result and print the values
                        while (rset.next()) {

                            databaseLoads++;

                            ConceptAction action = new ConceptAction();
                            action.ID_action = Integer.parseInt(rset.getObject(1).toString());
                            action.type = rset.getObject(2).toString();
                            action.persons = Integer.parseInt(rset.getObject(3).toString());
                            action.from = rset.getObject(4).toString();
                            action.to = rset.getObject(5).toString();
                            conceptActions.add(action);
                        }
                    } // close the ResultSet
                } // close the Statement
            } // close the connection

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {
                    // select something from the system's dual table
                    try (ResultSet rset = stmt.executeQuery(
                            "SELECT * FROM lyzarsky_zajezd")) {
                        // iterate through the result and print the values
                        while (rset.next()) {

                            databaseLoads++;

                            ConceptTour tour = new ConceptTour();
                            tour.ID_tour = Integer.parseInt(rset.getObject(1).toString());
                            tour.state = rset.getObject(2).toString();
                            tour.location = rset.getObject(3).toString();
                            tour.center = rset.getObject(4).toString();
                            tour.from = rset.getObject(5).toString();
                            tour.to = rset.getObject(6).toString();
                            tour.ID_hotel = Integer.parseInt(rset.getObject(7).toString());
                            conceptTours.add(tour);
                        }
                    } // close the ResultSet
                } // close the Statement
            } // close the connection

            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {
                    // select something from the system's dual table
                    try (ResultSet rset = stmt.executeQuery(
                            "SELECT * FROM objednavka_uzivatel")) {
                        // iterate through the result and print the values
                        while (rset.next()) {

                            databaseLoads++;

                            ConceptOrderUser orderUser = new ConceptOrderUser();

                            orderUser.ID_order_user = Integer.parseInt(rset.getObject(1).toString());
                            orderUser.ID_user = Integer.parseInt(rset.getObject(2).toString());
                            orderUser.ID_order = Integer.parseInt(rset.getObject(3).toString());

//                            orderUser.begining = rset.getObject(4).toString();
//                            orderUser.ending = rset.getObject(5).toString();

                            conceptOrderUsers.add(orderUser);
                        }
                    } // close the ResultSet
                } // close the Statement
            } // close the connection

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {
                    // select something from the system's dual table
                    try (ResultSet rset = stmt.executeQuery(
                            "SELECT * FROM objednavka")) {
                        // iterate through the result and print the values
                        while (rset.next()) {

                            databaseLoads++;

                            ConceptOrder order = new ConceptOrder();
                            order.ID_order = Integer.parseInt(rset.getObject(1).toString());

                            if (rset.getObject(2).toString().equalsIgnoreCase("Y"))
                                order.cancelled = true;
                            else
                                order.cancelled = false;

                            order.date = rset.getObject(3).toString();
//                            order.begining = rset.getObject(4).toString();
//                            order.ending = rset.getObject(5).toString();

                            conceptOrders.add(order);

                            ordersCount++;
                        }
                    } // close the ResultSet
                } // close the Statement
            } // close the connection

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {
                    // select something from the system's dual table
                    try (ResultSet rset = stmt.executeQuery(
                            "SELECT * FROM objednavka_zajezdu")) {
                        // iterate through the result and print the values
                        while (rset.next()) {

                            databaseLoads++;

                            ConceptOrderTour orderTour = new ConceptOrderTour();
                            orderTour.ID_order_tour = Integer.parseInt(rset.getObject(1).toString());
                            orderTour.ID_order = Integer.parseInt(rset.getObject(2).toString());
                            orderTour.ID_tour = Integer.parseInt(rset.getObject(3).toString());

                            if (rset.getObject(4).toString().equalsIgnoreCase("Y"))
                                orderTour.food = true;
                            else
                                orderTour.food = false;

                            if (rset.getObject(5).toString().equalsIgnoreCase("Y"))
                                orderTour.bus = true;
                            else
                                orderTour.bus = false;

                            orderTour.persons = Integer.parseInt(rset.getObject(6).toString());
                            conceptOrderTours.add(orderTour);

                            orderToursCount++;
                        }
                    } // close the ResultSet
                } // close the Statement
            } // close the connection

            // connect to the database
            try (Connection conn = ods.getConnection()) {
                // create a Statement
                try (Statement stmt = conn.createStatement()) {
                    // select something from the system's dual table
                    try (ResultSet rset = stmt.executeQuery(
                            "SELECT * FROM objednavka_doprovodne_akce")) {
                        // iterate through the result and print the values
                        while (rset.next()) {

                            databaseLoads++;

                            ConceptOrderAction orderAction = new ConceptOrderAction();
                            orderAction.ID_order_action = Integer.parseInt(rset.getObject(1).toString());
                            orderAction.ID_order_tour = Integer.parseInt(rset.getObject(2).toString());
                            orderAction.ID_action = Integer.parseInt(rset.getObject(3).toString());
                            conceptOrderActions.add(orderAction);

                            orderActionsCount++;
                        }
                    } // close the ResultSet
                } // close the Statement
            } // close the connection

        } catch (SQLException sqlEx) {
            System.err.println("SQLException: " + sqlEx.getMessage());
        }

        if (databaseLoads > 0)
        {
            int N;
            int M;
            N = conceptUsers.size();

            for (int i = 0; i < N; i++)
            {
                User user = new User();
                user.username = conceptUsers.get(i).login;
                user.password = conceptUsers.get(i).password;
                user.firstName = conceptUsers.get(i).firstName;
                user.lastName = conceptUsers.get(i).lastName;
                user.isMale = conceptUsers.get(i).isMale;
                user.identificationNumber = conceptUsers.get(i).identificationNumber;
                user.birthDate = conceptUsers.get(i).birthDate;
                user.phoneNumber = conceptUsers.get(i).phone;
                user.email = conceptUsers.get(i).email;
                user.address = conceptUsers.get(i).address;
                users.add(user);
            }

            N = conceptHotels.size();

            for (int i = 0; i < N; i++)
            {
                Hotel hotel = new Hotel();
                hotel.name = conceptHotels.get(i).name;
                hotel.stars = conceptHotels.get(i).stars;
                hotels.add(hotel);
                hotelsRestore.add(hotel);
            }

            N = conceptActions.size();

            for (int i = 0; i < N; i++)
            {
                Action action = new Action();
                action.name = conceptActions.get(i).type;
                action.persons = conceptActions.get(i).persons;
                action.from = conceptActions.get(i).from;
                action.to = conceptActions.get(i).to;
                actions.add(action);
            }

            N = conceptTours.size();

            for (int i = 0; i < N; i++)
            {
                Tour tour = new Tour();
                tour.state = conceptTours.get(i).state;
                tour.location = conceptTours.get(i).location;
                tour.center = conceptTours.get(i).center;
                tour.from = conceptTours.get(i).from;
                tour.to = conceptTours.get(i).to;
                tour.hotel.name = hotelsRestore.get(conceptTours.get(i).ID_hotel - 1).name;
                tour.hotel.stars = hotelsRestore.get(conceptTours.get(i).ID_hotel - 1).stars;
                tours.add(tour);
                toursRestore.add(tour);
            }

            N = conceptOrders.size();

            for (int i = 0; i < N; i++)
            {
                OrderPack orderPack = new OrderPack();

                M = conceptOrderUsers.size();
                int ID_user = 0;
                for (int j = 0; j < M; j++)
                {
                    if (conceptOrderUsers.get(j).ID_order == i + 1)
                    {
                        ID_user = conceptOrderUsers.get(j).ID_user;
                        break;
                    }
                }

                String login = conceptUsers.get(ID_user - 1).login;

                M = conceptOrderTours.size();

                for (int j = 0; j < M; j++)
                {
                    if (conceptOrderTours.get(j).ID_order == conceptOrders.get(i).ID_order)
                    {
                        Order order = new Order();
                        order.food = conceptOrderTours.get(j).food;
                        order.bus = conceptOrderTours.get(j).bus;
                        order.personCount = conceptOrderTours.get(j).persons;
                        order.tourIndex = conceptOrderTours.get(j).ID_tour - 1;

                        int O = conceptOrderActions.size();

                        for (int k = 0; k < O; k++)
                        {
                            if (conceptOrderTours.get(j).ID_order_tour == conceptOrderActions.get(k).ID_order_tour)
                            {
                                order.actionsIndices.add(conceptOrderActions.get(k).ID_action);
                            }
                        }

                        orderPack.orders.add(order);
                    }
                }

                orderPack.orderDate = conceptOrders.get(i).date;
                orderPack.accepted = conceptOrders.get(i).accepted;
                orderPack.cancelled = conceptOrders.get(i).cancelled;

                M = users.size();

                for (int j = 0; j < M; j++)
                {
                    if (users.get(j).username.equalsIgnoreCase(login))
                    {
                        users.get(j).orders.add(orderPack);
                        break;
                    }
                }
            }
        }
    }

    /**
     * Default initialize method which is going to be called after every startup of client application
     */
    @FXML
    public void initialize()
    {
        initFromDatabase();

        initTours();
        initHotels();
        initActions();
        initTray();

        handleLogin();
        applyEffects();

        tabs.getSelectionModel().selectedItemProperty().addListener((ov, oldTab, newTab) -> {
            int returnValue = tabs.getSelectionModel().getSelectedIndex();

            if (returnValue == 0)
            {
                actualTab = tabType.client;

                setPageSpinnerVisible(false);
                setFiltersVisible(false);
            }
            else if (returnValue == 1)
            {
                actualTab = tabType.orders;
                int N = users.get(loggedIn).orders.size();

                pageChangeAllowed = false;
                int oldIndex = ordersPageIndex;
                pageSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, N / 10 + 1));
                pageSpinner.getValueFactory().setValue(oldIndex + 1);
                pageChangeAllowed = true;

                setPageSpinnerVisible(true);
                setFiltersVisible(false);
            }
            else if (returnValue == 2)
            {
                actualTab = tabType.tours;
                int N = tours.size();

                pageChangeAllowed = false;
                int oldIndex = toursPageIndex;
                pageSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, N / 10 + 1));
                pageSpinner.getValueFactory().setValue(oldIndex + 1);
                pageChangeAllowed = true;

                setPageSpinnerVisible(true);
                setFiltersVisible(true);
            }
            else if (returnValue == 3)
            {
                actualTab = tabType.hotels;
                int N = hotels.size();

                pageChangeAllowed = false;
                int oldIndex = hotelsPageIndex;
                pageSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, N / 10 + 1));
                pageSpinner.getValueFactory().setValue(oldIndex + 1);
                pageChangeAllowed = true;

                setPageSpinnerVisible(true);
                setFiltersVisible(false);
            }
            else if (returnValue == 4)
            {
                actualTab = tabType.actions;
                int N = actions.size();

                pageChangeAllowed = false;
                int oldIndex = actionsPageIndex;
                pageSpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, N / 10 + 1));
                pageSpinner.getValueFactory().setValue(oldIndex + 1);
                pageChangeAllowed = true;

                setPageSpinnerVisible(true);
                setFiltersVisible(false);
            }
        });

        genderButton.setOnAction((event) -> {
            if (genderButton.getText().equalsIgnoreCase("Muž"))
                genderButton.setText("Žena");
            else
                genderButton.setText("Muž");
        });

        loginEdit.setOnAction(event -> {
            if (loggedIn == -1)
                handleLogin();
        });

        passwordEdit.setOnAction(event -> {
            if (loggedIn == -1)
                handleLogin();
        });

        acceptButton.setOnAction((event) -> {
            handleUserUpdate();
        });

        logoutButton.setOnAction((event) -> {
            handleLogin();
        });

        adminButton.setOnAction((event) -> {
            if (adminLogged)
            {
                loginEdit.setEditable(true);
                loginEdit.clear();

                passwordEdit.setVisible(true);
                passwordEdit.setManaged(true);
                passwordEdit.clear();

                logoutButton.setVisible(true);
                logoutButton.setManaged(true);

                acceptButton.setVisible(true);
                acceptButton.setManaged(true);

                imageRotateRightButton.setVisible(false);
                imageRotateRightButton.setManaged(false);
                imageRotateRightTooltip.setText("Rotace fotografie vpravo");

                adminButton.setText("Správce");
                adminLogged = false;
            }
            else
                loginEdit.setText("Admin");
        });

        imagePathButton.setOnAction((event) -> {
            handleImagePathButton();
        });

        imageRotateLeftButton.setOnAction((event) -> {
            handleImageRotateLeftButton();
        });

        imageRotateRightButton.setOnAction((event) -> {
            if (adminLogged)
                adminDatabaseInit();
            else
                handleImageRotateRightButton();
        });

        imageContrastDownButton.setOnAction((event) -> {
            handleImageContrastDownButton();
        });

        imageContrastUpButton.setOnAction((event) -> {
            handleImageContrastUpButton();
        });

        imageBrightnessDownButton.setOnAction((event) -> {
            handleImageBrightnessDownButton();
        });

        imageBrightnessUpButton.setOnAction((event) -> {
            handleImageBrightnessUpButton();
        });

        accountImage.setOnMouseClicked(event -> {
            handleImagePathButton();
        });

        orderTourSelectOne.setOnAction((event) -> {
            orderTourSelected(0, orderTourSelectOne.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectTwo.setOnAction((event) -> {
            orderTourSelected(1, orderTourSelectTwo.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectThree.setOnAction((event) -> {
            orderTourSelected(2, orderTourSelectThree.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectFour.setOnAction((event) -> {
            orderTourSelected(3, orderTourSelectFour.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectFive.setOnAction((event) -> {
            orderTourSelected(4, orderTourSelectFive.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectSix.setOnAction((event) -> {
            orderTourSelected(5, orderTourSelectSix.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectSeven.setOnAction((event) -> {
            orderTourSelected(6, orderTourSelectSeven.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectEight.setOnAction((event) -> {
            orderTourSelected(7, orderTourSelectEight.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectNine.setOnAction((event) -> {
            orderTourSelected(8, orderTourSelectNine.getSelectionModel().getSelectedIndex());
        });

        orderTourSelectTen.setOnAction((event) -> {
            orderTourSelected(9, orderTourSelectTen.getSelectionModel().getSelectedIndex());
        });

        orderAcceptOne.setOnAction((event) -> {
            handleOrderAccept(0);
        });

        orderAcceptTwo.setOnAction((event) -> {
            handleOrderAccept(1);
        });

        orderAcceptThree.setOnAction((event) -> {
            handleOrderAccept(2);
        });

        orderAcceptFour.setOnAction((event) -> {
            handleOrderAccept(3);
        });

        orderAcceptFive.setOnAction((event) -> {
            handleOrderAccept(4);
        });

        orderAcceptSix.setOnAction((event) -> {
            handleOrderAccept(5);
        });

        orderAcceptSeven.setOnAction((event) -> {
            handleOrderAccept(6);
        });

        orderAcceptEight.setOnAction((event) -> {
            handleOrderAccept(7);
        });

        orderAcceptNine.setOnAction((event) -> {
            handleOrderAccept(8);
        });

        orderAcceptTen.setOnAction((event) -> {
            handleOrderAccept(9);
        });

        pickTourButtonOne.setOnAction((event) -> {
            handleTourPick(0);
        });

        pickTourButtonTwo.setOnAction((event) -> {
            handleTourPick(1);
        });

        pickTourButtonThree.setOnAction((event) -> {
            handleTourPick(2);
        });

        pickTourButtonFour.setOnAction((event) -> {
            handleTourPick(3);
        });

        pickTourButtonFive.setOnAction((event) -> {
            handleTourPick(4);
        });

        pickTourButtonSix.setOnAction((event) -> {
            handleTourPick(5);
        });

        pickTourButtonSeven.setOnAction((event) -> {
            handleTourPick(6);
        });

        pickTourButtonEight.setOnAction((event) -> {
            handleTourPick(7);
        });

        pickTourButtonNine.setOnAction((event) -> {
            handleTourPick(8);
        });

        pickTourButtonTen.setOnAction((event) -> {
            handleTourPick(9);
        });

        pickHotelButtonOne.setOnAction((event) -> {
            handleHotelPick(0);
        });

        pickHotelButtonTwo.setOnAction((event) -> {
            handleHotelPick(1);
        });

        pickHotelButtonThree.setOnAction((event) -> {
            handleHotelPick(2);
        });

        pickHotelButtonFour.setOnAction((event) -> {
            handleHotelPick(3);
        });

        pickHotelButtonFive.setOnAction((event) -> {
            handleHotelPick(4);
        });

        pickHotelButtonSix.setOnAction((event) -> {
            handleHotelPick(5);
        });

        pickHotelButtonSeven.setOnAction((event) -> {
            handleHotelPick(6);
        });

        pickHotelButtonEight.setOnAction((event) -> {
            handleHotelPick(7);
        });

        pickHotelButtonNine.setOnAction((event) -> {
            handleHotelPick(8);
        });

        pickHotelButtonTen.setOnAction((event) -> {
            handleHotelPick(9);
        });

        insertButton.setOnAction((event) -> {
            handleOrderPick();
        });

        foodCheckOne.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 0).food = foodCheckOne.isSelected();
        });

        foodCheckTwo.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 1).food = foodCheckTwo.isSelected();
        });

        foodCheckThree.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 2).food = foodCheckThree.isSelected();
        });

        foodCheckFour.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 3).food = foodCheckFour.isSelected();
        });

        foodCheckFive.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 4).food = foodCheckFive.isSelected();
        });

        foodCheckSix.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 5).food = foodCheckSix.isSelected();
        });

        foodCheckSeven.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 6).food = foodCheckSeven.isSelected();
        });

        foodCheckEight.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 7).food = foodCheckEight.isSelected();
        });

        foodCheckNine.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 8).food = foodCheckNine.isSelected();
        });

        foodCheckTen.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 9).food = foodCheckTen.isSelected();
        });

        busCheckOne.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 0).bus = busCheckOne.isSelected();
        });

        busCheckTwo.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 1).bus = busCheckTwo.isSelected();
        });

        busCheckThree.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 2).bus = busCheckThree.isSelected();
        });

        busCheckFour.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 3).bus = busCheckFour.isSelected();
        });

        busCheckFive.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 4).bus = busCheckFive.isSelected();
        });

        busCheckSix.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 5).bus = busCheckSix.isSelected();
        });

        busCheckSeven.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 6).bus = busCheckSeven.isSelected();
        });

        busCheckEight.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 7).bus = busCheckEight.isSelected();
        });

        busCheckNine.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 8).bus = busCheckNine.isSelected();
        });

        busCheckTen.setOnAction((event) -> {
            tours.get(toursPageIndex * 10 + 9).bus = busCheckTen.isSelected();
        });

        actionCheckOne.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 0).want = actionCheckOne.isSelected();
        });

        actionCheckTwo.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 1).want = actionCheckTwo.isSelected();
        });

        actionCheckThree.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 2).want = actionCheckThree.isSelected();
        });

        actionCheckFour.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 3).want = actionCheckFour.isSelected();
        });

        actionCheckFive.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 4).want = actionCheckFive.isSelected();
        });

        actionCheckSix.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 5).want = actionCheckSix.isSelected();
        });

        actionCheckSeven.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 6).want = actionCheckSeven.isSelected();
        });

        actionCheckEight.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 7).want = actionCheckEight.isSelected();
        });

        actionCheckNine.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 8).want = actionCheckNine.isSelected();
        });

        actionCheckTen.setOnAction((event) -> {
            actions.get(actionsPageIndex * 10 + 9).want = actionCheckTen.isSelected();
        });

        filterState.setOnAction(event -> {
            handleFilter();
        });

        filterLocation.setOnAction(event -> {
            handleFilter();
        });

        filterCenter.setOnAction(event -> {
            handleFilter();
        });

        filterFrom.valueProperty().addListener((ov, oldValue, newValue) -> {
            handleFilter();
        });

        filterTo.valueProperty().addListener((ov, oldValue, newValue) -> {
            handleFilter();
        });

        similarityButton.setOnAction((event) -> {
            handleSimilarity();
        });

        pageSpinner.valueProperty().addListener((obs, oldValue, newValue) -> {
            handlePageChange(newValue);
        });
    }
}
