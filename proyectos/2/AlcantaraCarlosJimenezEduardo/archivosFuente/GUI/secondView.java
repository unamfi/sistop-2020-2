package GUI;

import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

// @Author: Alcantara Hoyos Carlos Eduardo & Jimenez Gonzalez Jose Eduardo

public class secondView extends javax.swing.JFrame {

    public secondView() {
        initComponents();
        setAlert(false);
    }

    // Definicion de todos los componentes graficos de la GUI, asi la declaracion de los manejadores de eventos en mouse para los botones.
    
    private void initComponents() {

        jPanel1 = new javax.swing.JPanel();
        warningLabel = new javax.swing.JLabel();
        E1 = new javax.swing.JLabel();
        E2 = new javax.swing.JLabel();
        E3 = new javax.swing.JLabel();
        E4 = new javax.swing.JLabel();
        E5 = new javax.swing.JLabel();
        E6 = new javax.swing.JLabel();
        E7 = new javax.swing.JLabel();
        E8 = new javax.swing.JLabel();
        E9 = new javax.swing.JLabel();
        E10 = new javax.swing.JLabel();
        E11 = new javax.swing.JLabel();
        E12 = new javax.swing.JLabel();
        E13 = new javax.swing.JLabel();
        E14 = new javax.swing.JLabel();
        E15 = new javax.swing.JLabel();
        E16 = new javax.swing.JLabel();
        E17 = new javax.swing.JLabel();
        E18 = new javax.swing.JLabel();
        E19 = new javax.swing.JLabel();
        E20 = new javax.swing.JLabel();
        E21 = new javax.swing.JLabel();
        E22 = new javax.swing.JLabel();
        E23 = new javax.swing.JLabel();
        E24 = new javax.swing.JLabel();
        E25 = new javax.swing.JLabel();
        startB = new javax.swing.JLabel();
        countPeopleField = new javax.swing.JTextField();
        jLabel3 = new javax.swing.JLabel();
        counterCola = new javax.swing.JLabel();
        enqueuePeople = new javax.swing.JLabel();
        upperBar = new javax.swing.JLabel();
        termPanel = new javax.swing.JLabel();
        alertLabel = new javax.swing.JLabel();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setBackground(new java.awt.Color(255, 255, 255));
        setResizable(false);

        jPanel1.setBackground(new java.awt.Color(255, 255, 255));
        jPanel1.setLayout(null);

        warningLabel.setForeground(new java.awt.Color(255, 255, 255));
        warningLabel.setText("Ingresa el numero de pasajeros (= , y presiona Play.");
        jPanel1.add(warningLabel);
        warningLabel.setBounds(380, 50, 330, 16);

        E1.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E1.png"))); 
        jPanel1.add(E1);
        E1.setBounds(250, 400, 110, 50);

        E2.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E2.png"))); 
        jPanel1.add(E2);
        E2.setBounds(330, 380, 110, 50);

        E3.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E3.png"))); 
        jPanel1.add(E3);
        E3.setBounds(390, 370, 110, 50);

        E4.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E4.png"))); 
        jPanel1.add(E4);
        E4.setBounds(460, 380, 110, 50);

        E5.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E5.png"))); 
        jPanel1.add(E5);
        E5.setBounds(530, 360, 120, 50);

        E6.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E6.png"))); 
        jPanel1.add(E6);
        E6.setBounds(580, 330, 110, 50);

        E7.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E7.png"))); 
        jPanel1.add(E7);
        E7.setBounds(600, 240, 110, 100);

        E8.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E8.png"))); 
        jPanel1.add(E8);
        E8.setBounds(580, 190, 110, 100);

        E9.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E9.png"))); 
        jPanel1.add(E9);
        E9.setBounds(510, 210, 110, 100);

        E10.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E10.png"))); 
        jPanel1.add(E10);
        E10.setBounds(460, 250, 110, 100);

        E11.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E11.png"))); 
        jPanel1.add(E11);
        E11.setBounds(390, 300, 110, 100);

        E12.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E12.png"))); 
        jPanel1.add(E12);
        E12.setBounds(330, 300, 110, 100);

        E13.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E13.png"))); 
        jPanel1.add(E13);
        E13.setBounds(260, 290, 110, 100);

        E14.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E14.png"))); 
        jPanel1.add(E14);
        E14.setBounds(190, 260, 110, 90);

        E15.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E15.png"))); 
        jPanel1.add(E15);
        E15.setBounds(110, 220, 110, 100);

        E16.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E16.png"))); 
        jPanel1.add(E16);
        E16.setBounds(60, 210, 110, 60);

        E17.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E17.png"))); 
        jPanel1.add(E17);
        E17.setBounds(60, 160, 110, 60);

        E18.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E18.png"))); 
        jPanel1.add(E18);
        E18.setBounds(100, 130, 110, 60);

        E19.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E19.png"))); 
        jPanel1.add(E19);
        E19.setBounds(150, 160, 110, 60);

        E20.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E20.png"))); 
        jPanel1.add(E20);
        E20.setBounds(160, 190, 110, 90);

        E21.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E21.png"))); 
        jPanel1.add(E21);
        E21.setBounds(40, 230, 110, 90);

        E22.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E22.png"))); 
        jPanel1.add(E22);
        E22.setBounds(-10, 260, 110, 100);

        E23.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E23.png"))); 
        jPanel1.add(E23);
        E23.setBounds(20, 300, 110, 90);

        E24.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E24.png"))); 
        jPanel1.add(E24);
        E24.setBounds(80, 300, 110, 110);

        E25.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/vagones estados/E25.png"))); 
        jPanel1.add(E25);
        E25.setBounds(150, 290, 110, 110);

        startB.addMouseListener(new MouseAdapter() // Declaracion de manejador de eventos del boton play. 
            {
                public void mouseClicked(MouseEvent e)
                {
                    startBmouseClicked(e);

                }
            });
            jPanel1.add(startB);
            startB.setBounds(70, 20, 60, 70);

            countPeopleField.setHorizontalAlignment(javax.swing.JTextField.CENTER);
            countPeopleField.setBorder(null);
            countPeopleField.addActionListener(new java.awt.event.ActionListener() {
                public void actionPerformed(java.awt.event.ActionEvent evt) {
                    countPeopleFieldActionPerformed(evt);
                }
            });
            jPanel1.add(countPeopleField);
            countPeopleField.setBounds(190, 50, 150, 20);

            jLabel3.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/1.png"))); // NOI18N
            jPanel1.add(jLabel3);
            jLabel3.setBounds(10, 130, 690, 460);

            counterCola.setFont(new java.awt.Font("Lucida Grande", 0, 36)); 
            counterCola.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
            counterCola.setText("0");
            jPanel1.add(counterCola);
            counterCola.setBounds(830, 370, 50, 60);

            enqueuePeople.setFont(new java.awt.Font("SF Compact Rounded", 0, 18)); // NOI18N
            enqueuePeople.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/enqueuePeople.png"))); // NOI18N
            jPanel1.add(enqueuePeople);
            enqueuePeople.setBounds(790, 310, 130, 150);

            upperBar.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/upperBar.png"))); // NOI18N
            jPanel1.add(upperBar);
            upperBar.setBounds(50, 10, 890, 100);

            termPanel.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/terms.png"))); // NOI18N
            jPanel1.add(termPanel);
            termPanel.setBounds(730, 120, 250, 170);

            alertLabel.setIcon(new javax.swing.ImageIcon(getClass().getResource("/icon/alert.png"))); // NOI18N
            jPanel1.add(alertLabel);
            alertLabel.setBounds(745, 460, 220, 90);

            javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
            getContentPane().setLayout(layout);
            layout.setHorizontalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, 1004, Short.MAX_VALUE)
            );
            layout.setVerticalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, 576, Short.MAX_VALUE)
            );

            pack();
        }

    private void countPeopleFieldActionPerformed(java.awt.event.ActionEvent evt) {
        // Metodo creado para mantener el textField.
    }

    public void setCar(int onCar, int offCar) {

        switch (onCar) {
            case 1:
                E1.setVisible(true);
                break;
            case 2:
                E2.setVisible(true);
                break;
            case 3:
                E3.setVisible(true);
                break;
            case 4:
                E4.setVisible(true);
                break;
            case 5:
                E5.setVisible(true);
                break;
            case 6:
                E6.setVisible(true);
                break;
            case 7:
                E7.setVisible(true);
                break;
            case 8:
                E8.setVisible(true);
                break;
            case 9:
                E9.setVisible(true);
                break;
            case 10:
                E10.setVisible(true);
                break;
            case 11:
                E11.setVisible(true);
                break;
            case 12:
                E12.setVisible(true);
                break;
            case 13:
                E13.setVisible(true);
                break;
            case 14:
                E14.setVisible(true);
                break;
            case 15:
                E15.setVisible(true);
                break;
            case 16:
                E16.setVisible(true);
                break;
            case 17:
                E17.setVisible(true);
                break;
            case 18:
                E18.setVisible(true);
                break;
            case 19:
                E19.setVisible(true);
                break;
            case 20:
                E20.setVisible(true);
                break;
            case 21:
                E21.setVisible(true);
                break;
            case 22:
                E22.setVisible(true);
                break;
            case 23:
                E23.setVisible(true);
                break;
            case 24:
                E24.setVisible(true);
                break;
            case 25:
                E25.setVisible(true);
                break;
            default:
                break;
        }

        switch (offCar) {
            case 1:
                E1.setVisible(false);
                break;
            case 2:
                E2.setVisible(false);
                break;
            case 3:
                E3.setVisible(false);
                break;
            case 4:
                E4.setVisible(false);
                break;
            case 5:
                E5.setVisible(false);
                break;
            case 6:
                E6.setVisible(false);
                break;
            case 7:
                E7.setVisible(false);
                break;
            case 8:
                E8.setVisible(false);
                break;
            case 9:
                E9.setVisible(false);
                break;
            case 10:
                E10.setVisible(false);
                break;
            case 11:
                E11.setVisible(false);
                break;
            case 12:
                E12.setVisible(false);
                break;
            case 13:
                E13.setVisible(false);
                break;
            case 14:
                E14.setVisible(false);
                break;
            case 15:
                E15.setVisible(false);
                break;
            case 16:
                E16.setVisible(false);
                break;
            case 17:
                E17.setVisible(false);
                break;
            case 18:
                E18.setVisible(false);
                break;
            case 19:
                E19.setVisible(false);
                break;
            case 20:
                E20.setVisible(false);
                break;
            case 21:
                E21.setVisible(false);
                break;
            case 22:
                E22.setVisible(false);
                break;
            case 23:
                E23.setVisible(false);
                break;
            case 24:
                E24.setVisible(false);
                break;
            case 25:
                E25.setVisible(false);
                break;
            default:
                break;
        }
    } // Metodo que se encarga del movimiento del vagon en la GUI.

    
    public void setAlert(Boolean b){
        alertLabel.setVisible(b);
    } 
            
            
    public void setAmout(int number){
        counterCola.setText(""+number);
    } // Se encarga de manejar el contador, de personas en cola.
    
    public int getAmout(){ 
       return Integer.parseInt(counterCola.getText());
    } // Obtiene la cantidad de personas actuales en cola.
    
    private void startBmouseClicked(MouseEvent e) {
        String s = countPeopleField.getText();
        if (s.isEmpty()) {
            warningLabel.setText("El valor debe estar entre 3 y 200.");
        } else {

            try {
                int amount = Integer.parseInt(s);
                if (amount >= 4 && amount <= 200) {
                    warningLabel.setText("");
                    startB.setEnabled(false);
                    E1.setVisible(true);
                    E2.setVisible(false);
                    E3.setVisible(false);
                    E4.setVisible(false);
                    E5.setVisible(false);
                    E6.setVisible(false);
                    E7.setVisible(false);
                    E8.setVisible(false);
                    E9.setVisible(false);
                    E10.setVisible(false);
                    E11.setVisible(false);
                    E12.setVisible(false);
                    E13.setVisible(false);
                    E14.setVisible(false);
                    E15.setVisible(false);
                    E16.setVisible(false);
                    E17.setVisible(false);
                    E18.setVisible(false);
                    E19.setVisible(false);
                    E20.setVisible(false);
                    E21.setVisible(false);
                    E22.setVisible(false);
                    E23.setVisible(false);
                    E24.setVisible(false);
                    E25.setVisible(false);
                    counterCola.setText(""+amount);
                    Prueba.mainRun(this,amount);
        
                    
                } else {
                    warningLabel.setText("El valor debe estar entre 4 y 200.");
                }

            } catch (NumberFormatException ex) {
                warningLabel.setText("El valor debe ser numerico.");
            }
            
            startB.setEnabled(true);
            

        }
    } 

   
    public static void main(String args[]) {
     
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(secondView.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(secondView.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(secondView.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(secondView.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
       
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new secondView().setVisible(true); // Crea un hilo para la ventana, y la muestra una vez todos sus companentes ya hayan cargado.
                
            }
        });
    }


    private javax.swing.JLabel E1;
    private javax.swing.JLabel E10;
    private javax.swing.JLabel E11;
    private javax.swing.JLabel E12;
    private javax.swing.JLabel E13;
    private javax.swing.JLabel E14;
    private javax.swing.JLabel E15;
    private javax.swing.JLabel E16;
    private javax.swing.JLabel E17;
    private javax.swing.JLabel E18;
    private javax.swing.JLabel E19;
    private javax.swing.JLabel E2;
    private javax.swing.JLabel E20;
    private javax.swing.JLabel E21;
    private javax.swing.JLabel E22;
    private javax.swing.JLabel E23;
    private javax.swing.JLabel E24;
    private javax.swing.JLabel E25;
    private javax.swing.JLabel E3;
    private javax.swing.JLabel E4;
    private javax.swing.JLabel E5;
    private javax.swing.JLabel E6;
    private javax.swing.JLabel E7;
    private javax.swing.JLabel E8;
    private javax.swing.JLabel E9;
    private javax.swing.JLabel alertLabel;
    private javax.swing.JTextField countPeopleField;
    private javax.swing.JLabel counterCola;
    private javax.swing.JLabel enqueuePeople;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JLabel startB;
    private javax.swing.JLabel termPanel;
    private javax.swing.JLabel upperBar;
    private javax.swing.JLabel warningLabel;
    
}
