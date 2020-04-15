# coding: utf-8
class EjemploHilos
  def initialize
    @x = 0
  end
  
  def run
    t1 = Thread.new {f1}
    t2 = Thread.new {f2(t1)}
    sleep 0.1
    t2.join
    print ' %d ' % @x
  end

  def f1
    sleep 0.1
    print '+'
    @x += 3
  end
  
  def f2(t)
    sleep 0.1
    t.join
    print '*'
    @x *= 2
  end
end

e = EjemploHilos.new;10.times{e.run}
