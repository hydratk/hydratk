package jmsclient;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Properties;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.jms.ConnectionFactory;
import javax.jms.Queue;
import javax.jms.Connection;
import javax.jms.Session;
import javax.jms.MessageProducer;
import javax.jms.TextMessage;

/**
* Generic wrapper to JMS clients
* Specific client libraries are located in lib folder
* Supported clients - WebLogic (weblogic.jar)
* 
* @author  Petr Rašek
* @version 0.1.0
* @since   2015-11-15 
*/

public class JMSClient {

    static boolean running = true;
    static Context ctx = null;
    static Connection connection = null;
    static ConnectionFactory factory = null;
    static Session session = null;
    static MessageProducer producer = null;     
    
    public static void main(String[] args) {
        
        try {
            
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));             
            String[] input;
            String command;
            HashMap<String, String> params = null;                       
            
            while (running) {
                
                input = br.readLine().split("&&&");
                command = input[0];              
                
                if (input.length > 1) {
                    
                    params = new HashMap();
                    
                    for (int i = 1; i < input.length; i=i+2) 
                        params.put(input[i], input[i+1]);

                }
                
                switch (command) {
                    
                    case "connect":
                        connect(params);
                        break;
                    
                    case "disconnect":
                        disconnect();
                        break;
                        
                    case "send":
                        send(params);
                        break;
                        
                    default:
                        System.out.println("ERR - Unknown command:" + command);
                        break;
                    
                }
            
            }
           
            System.exit(0);
        
        }
        catch (Exception ex) {
            
            System.out.println(ex);
            
        }
        
    }
    
    /**
    * connect
    * Connect to JMS server
    * @param params - connectionFactory, initialContextFactory, providerURL,
    *                 securityPrincipal, securityCredentials
    */    
    public static void connect(HashMap<String, String> params) {
        
        try {
        
            System.out.println("INFO - Received command connect - params: " + params.toString());
            
            Properties properties = new Properties();
            properties.put(Context.PROVIDER_URL, params.get("providerURL"));
            properties.put(Context.INITIAL_CONTEXT_FACTORY, params.get("initialContextFactory")); 
            
            String user = params.get("securityPrincipal");
            if (user != null)
                properties.put(Context.SECURITY_PRINCIPAL, user);
            
            String pass = params.get("securityCredentials");
            if (pass != null)
                properties.put(Context.SECURITY_CREDENTIALS, pass);            
            
            ctx = new InitialContext(properties);            
            factory = (ConnectionFactory) ctx.lookup(params.get("connectionFactory"));
            connection = factory.createConnection();
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE); 
            System.out.println("OK - Connected to server");
        }
        catch (Exception ex) {
            
            System.out.println("ERR - " + ex);         
            
        }
        
    }
    
    /**
    * disconnect  
    * Disconnect from JMS server
    */      
    public static void disconnect() {
        
        try {
        
            System.out.println("INFO - Received command disconnect");
            
            if (producer != null)
                producer.close();
            
            if (session != null)
                session.close();
            
            if (connection != null)
                connection.close();  
                        
            running = false;
            System.out.println("OK - Disconnected from server");
            
        } 
        catch (Exception ex) {
            
            System.out.println("ERR - " + ex); 
            
        }
        
    }
    
    /**
    * send
    * Send JMS message
    * @param params - destination, JMSType, JMSCorrelationID, message 
    */      
    public static void send(HashMap<String, String> params) {
       
        try {
            
            System.out.println("INFO - Received command send - params: " + params.toString());
            
            Queue queue = (Queue)ctx.lookup(params.get("destination"));
            producer = session.createProducer(queue);
            
            TextMessage message = session.createTextMessage();
            message.setJMSCorrelationID(params.get("JMSCorrelationID"));
            message.setJMSType(params.get("JMSType"));
            message.setText(params.get("message"));  
            producer.send(message);
            System.out.println("OK - Message sent");
            
        }
        catch (Exception ex) {
            
            System.out.println("ERR - " + ex); 
            
        }
        
    }
    
}
