package cz.vutbr.fit.pdb.project01;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import oracle.jdbc.OracleDriver;
import oracle.jdbc.pool.OracleDataSource;

import javafx.application.Application;

/**
 * Client application class which executes the JavaFX rendering loop
 * @author Richard Hauerland
 */
public class App {

    /**
     * Main method which pass application parameters
     * @param Application parameters saved as a string array
     */
    public static void main(String[] args) throws Exception {

        Application.launch(sample.Main.class, args);
    }
}
