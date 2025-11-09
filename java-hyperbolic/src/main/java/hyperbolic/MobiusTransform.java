package hyperbolic;

/**
 * Möbius 변환: z -> (az + b) / (cz + d)
 */
public class MobiusTransform {
    private final Complex a, b, c, d;

    public MobiusTransform(Complex a, Complex b, Complex c, Complex d) {
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
    }

    public Complex apply(Complex z) {
        Complex numerator = a.mul(z).add(b);
        Complex denominator = c.mul(z).add(d);
        return numerator.div(denominator);
    }

    public static MobiusTransform identity() {
        return new MobiusTransform(
            Complex.one(), Complex.zero(),
            Complex.zero(), Complex.one()
        );
    }

    public static MobiusTransform translation(Complex z) {
        Complex zConj = z.conjugate();
        return new MobiusTransform(
            new Complex(1, 0),
            z.scale(-1),
            zConj.scale(-1),
            new Complex(1, 0)
        );
    }
}
