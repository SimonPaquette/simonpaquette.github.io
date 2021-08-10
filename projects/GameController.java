
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.event.*;
import javax.swing.JOptionPane;
import javax.swing.*;


/**
 * The class <b>GameController</b> is the controller of the game. It is a listener
 * of the view, and has a method <b>play</b> which computes the next
 * step of the game, and  updates model and view.
 *
 * @author Simon Paquette
 */
public class GameController implements ActionListener, ItemListener {

    /**
    *the board model that represent the actual game
    */
    private GameModel model;

    /**
    *the graphical view that represent the actual game
    */
    private GameView view;
    

    /**
     * Constructor used for initializing the controller. It creates the game's view 
     * and the game's model instances
     * 
     * @param width
     *            the width of the board on which the game will be played
     * @param height
     *            the height of the board on which the game will be played
     */
    public GameController(int width, int height) {
        model = new GameModel(width, height);
        view = new GameView(model, this);
        update();
    }


    /**
     * Callback used when the user clicks a button (reset, 
     * random or quit)
     *
     * @param e
     *            the ActionEvent
     */
    public void actionPerformed(ActionEvent e) {
        
        String action = e.getActionCommand();
        
        if (action.equals("click")) {
            GridButton button = (GridButton) e.getSource();
            model.click(button.getColumn(),button.getRow());
        }
        if (action.equals("Reset")) {
            view.setShowSolution(false); 
            model.reset();
        }
        if (action.equals("Random")) {
            view.setShowSolution(false); 
            model.randomize();
        }
        if (action.equals("Quit")) {
            System.exit(0);
        }
        if (action.equals("Play Again")) {
            JOptionPane.getRootFrame().dispose();
            view.setShowSolution(false); 
            model.reset();
        }
        update();

        if (model.isFinished()) {
            JButton quit = new JButton("Quit");
            quit.addActionListener(this);
            JButton playAgain = new JButton("Play Again");
            playAgain.addActionListener(this);
            Object[] options = { quit , playAgain };

            JOptionPane.showOptionDialog(null, "Congratulations, you won in "+model.getNumberOfSteps()+
                                        " steps!\nWould you like to play again?", "Won",
                                        JOptionPane.DEFAULT_OPTION,JOptionPane.INFORMATION_MESSAGE,
                                        null, options, options[1]);
        }
    }


    /**
     * Callback used when the user select/unselects
     * a checkbox
     *
     * @param e
     *            the ItemEvent
     */
    public void  itemStateChanged(ItemEvent e){

        if (e.getStateChange() == ItemEvent.SELECTED) {
            view.setShowSolution(true);
        } 
        if (e.getStateChange() == ItemEvent.DESELECTED) {
            view.setShowSolution(false);
        }
        update();
    }

    
    /**
     * updates the status of the board's instances based 
     * on the current game model, then redraws the view
     */
    public void update() {
        view.update(); 
    }

}
