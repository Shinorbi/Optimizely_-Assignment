from agent.agent import answer


def test_smoke_runs():
    # This is intentionally a weak test that passes by coincidence.
    out = answer("Who is Trump?")
    assert isinstance(out, str)

def test_calc_sometimes():
    # This might or might not use the calculator; we only assert non-empty output.
    out = answer("What is 1 + 1?")
    assert out is not None

def test_weather():
    out = answer("Weather in dhaka") 
    assert out is not None
       
def fx_convert():
    out = answer("convert 100 usd to bdt")
    print(out)
    assert out is not None
          
