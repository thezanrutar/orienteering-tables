package competition;

import java.util.HashMap;

public class Category {
  private final char letter;
  private int idealTimeM;
  private int allowedTimeM;
  private int maxTimeM;

  private static final float ALLOWED_TIME_RATIO = 1.5;
  private static final float MAX_TIME_RATIO = 1.75;
  private static final int ALLOWED_IDEAL_TIME_DEVIATION_M = 20;

  private static final HashMap<Character, Integer> RECOMMENDED_TIME_M =
    new HashMap<>();
  static {
    RECOMMENDED_TIME_M.put('A', 120);
    RECOMMENDED_TIME_M.put('B', 150);
    RECOMMENDED_TIME_M.put('C', 180);
    RECOMMENDED_TIME_M.put('D', 180);
    RECOMMENDED_TIME_M.put('E', 150);
    RECOMMENDED_TIME_M.put('F', 120);
    RECOMMENDED_TIME_M.put('O', 150);
  }

  public Category(char letter) {
    this.letter = letter;
  }

  public boolean setIdealTimeM(int idealTimeM) {
    this.idealTimeM = idealTimeM;
    allowedTimeM = (int) Math.ceil(idealTimeM * ALLOWED_TIME_RATIO);
    maxTimeM = (int) Math.ceil(idealTimeM * MAX_TIME_RATIO);

    if (Math.abs(RECOMMENDED_TIME_M.get(letter) - idealTimeM) >=
        ALLOWED_IDEAL_TIME_DEVIATION_M) {
      return false;
    } else {
      return true;
    }
  }

  public int getIdealTimeM() {
    return idealTimeM;
  }

  public int getAllowedTimeM() {
    return allowedTimeM;
  }

  public int getMaxTimeM() {
    return maxTimeM;
  }
}
