/*
by 韻帆
設定t在時間的1/2處做reset，
 */

import java.util.ArrayList;
import java.util.Random;

public class Reset_Options {
    public static ArrayList<Double> resetPutPrice (double S0, double K, double T, double sd, double r, double n){
        Random ran = new Random();
        double dt = T/n;
        double sumOfChange = 0;
        double resetPrice = 0;
        double stockPrice = 0;
        for( int i = 0; i < n; i++ ){
            // 隨機從normal抽值
            double nd = ran.nextGaussian();
            double dz = nd * (Math.sqrt(dt));
            double logPriceChange = (r - Math.pow(sd, 2)/2) * dt + sd * dz;
            sumOfChange += logPriceChange;
            double logStockPrice = Math.log(S0) + sumOfChange;
            stockPrice = Math.exp(logStockPrice);

            if ( i > n/2 - 1 &&  i < n/2 + 1) {
                resetPrice = stockPrice;
            }
        }
        double strikePrice = Math.max(resetPrice, K);
        double resetPut = Math.max(strikePrice - stockPrice, 0);
        double originPut = Math.max(K - stockPrice, 0);
        ArrayList<Double> bothArr = new ArrayList<>();
        bothArr.add(resetPut);
        bothArr.add(originPut);
        return bothArr;
    }

    // using monte carlo to price the reset option 
    public static Double MonteRPutPrice(double S0, double K, double T, double sd, double r, double n, int test){
//        ArrayList<Double> arrayListPut = new ArrayList<>();
        double sumOfRPutPrice = 0;
        for (int i = 0; i < test; i++){
            double resetPutP = resetPutPrice(S0, K, T, sd, r, n).get(0);
            sumOfRPutPrice += resetPutP;
//            arrayListPut.add(resetPutP);
        }
        double AverRPrice = sumOfRPutPrice / test;
        double finalAverRPutPrice = Math.exp(-1 * r * T) * AverRPrice;

        return finalAverRPutPrice;
    }
    
    // using monte carlo to price the vanilla option
    public static Double MonteOPutPrice(double S0, double K, double T, double sd, double r, double n, int test){
//        ArrayList<Double> arrayListPut = new ArrayList<>();
        double sumOfOPutPrice = 0;
        for (int i = 0; i < test; i++){
            double originPutP = resetPutPrice(S0, K, T, sd, r, n).get(1);
            sumOfOPutPrice += originPutP;
//            arrayListPut.add(resetPutP);
        }
        double AverOPrice = sumOfOPutPrice / test;
        double finalAverOPutPrice = Math.exp(-1 * r * T) * AverOPrice;

        return finalAverOPutPrice;
    }

    public static void main(String[] args) {
        for (int i = 0; i <= 100; i++){
            double rp0 = MonteRPutPrice(50, 50, 1, 0.25, 0.1, 2000, 10000);
            double op0 = MonteOPutPrice(50, 50, 1, 0.25, 0.1, 2000, 10000);
            System.out.println("Reset_PutPrice");
            System.out.print(rp0 + " ");
            System.out.println("origin_PutPrice");
            System.out.print(op0 + " ");
        }
    }

}