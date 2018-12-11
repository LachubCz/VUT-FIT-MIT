package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.File;
import java.nio.file.Paths;

/**
 * Required main class which is backbone of JavaFX logic
 * @author Richard Hauerland
 */
public class Main extends Application {

    /**
     * Loader of FXML source file with client frontend description
     */
    FXMLLoader fxmlLoader = new FXMLLoader();

    /**
     * Method which begins the JavaFX stage rendering
     * @param Stage object
     */
    @Override
    public void start(Stage primaryStage) throws Exception{

        String relativePath = "src/main/java/cz/vutbr/fit/pdb/project01/sample/sample.fxml";
        String absolutePath = "";

        File f = new File(relativePath);

        if (f.exists())
            absolutePath = f.getAbsoluteFile().toString();

        Parent root = fxmlLoader.load(Paths.get(absolutePath).toUri().toURL());

        primaryStage.setTitle("Lyžařské zájezdy");
        primaryStage.setScene(new Scene(root, 1024, 600));
        primaryStage.setMinWidth(1024);
        primaryStage.setMinHeight(600);
        primaryStage.setWidth(1024);
        primaryStage.setHeight(600);
        primaryStage.show();
    }

    /**
     * Main method which pass application parameters
     * @param Application parameters saved as a string array
     */
    public static void main(String[] args) {
        launch(args);
    }
}
