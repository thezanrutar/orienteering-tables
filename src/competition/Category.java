package competition;

import java.util.HashMap;

public class Category {
  private final char letter;
  private int idealTimeM;
  private int allowedTimeM;
  private int maxTimeM;

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

  public int addIdealTimeM(int idealTimeM) {
    this.idealTimeM = idealTimeM;
    allowedTimeM = (int) Math.ceil(idealTimeM * 1.5);
    maxTimeM = (int) Math.ceil(idealTimeM * 1.75);

    if (Math.abs(RECOMMENDED_TIME_M.get(letter) - idealTimeM) >= 20) {
      return 1;
    } else {
      return 0;
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
