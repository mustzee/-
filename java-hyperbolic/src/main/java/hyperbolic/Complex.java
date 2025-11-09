package hyperbolic;

/**
 * 복소수 클래스
 */
public class Complex {
    public final double re;
    public final double im;

    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    public static Complex zero() {
        return new Complex(0, 0);
    }

    public static Complex one() {
        return new Complex(1, 0);
    }

    public Complex add(Complex z) {
        return new Complex(this.re + z.re, this.im + z.im);
    }

    public Complex sub(Complex z) {
        return new Complex(this.re - z.re, this.im - z.im);
    }

    public Complex mul(Complex z) {
        return new Complex(
            this.re * z.re - this.im * z.im,
            this.re * z.im + this.im * z.re
        );
    }

    public Complex div(Complex z) {
        double denom = z.re * z.re + z.im * z.im;
        return new Complex(
            (this.re * z.re + this.im * z.im) / denom,
            (this.im * z.re - this.re * z.im) / denom
        );
    }

    public Complex conjugate() {
        return new Complex(this.re, -this.im);
    }

    public double abs() {
        return Math.sqrt(this.re * this.re + this.im * this.im);
    }

    public Complex scale(double s) {
        return new Complex(this.re * s, this.im * s);
    }

    public static Complex fromPolar(double r, double theta) {
        return new Complex(r * Math.cos(theta), r * Math.sin(theta));
    }

    @Override
    public String toString() {
        return String.format("%.3f + %.3fi", re, im);
    }
}
