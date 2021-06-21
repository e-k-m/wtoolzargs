# wtoolzargs

![](https://github.com/e-k-m/wtoolzargs/workflows/main/badge.svg)

> wtoolzargs contains core filtering and ordering logic for web applications

[Installation](#installation) | [Getting Up And Running](#getting-up-and-running) | [Examples](#examples) | [API](#api) | [See Also](#see-also)

wtoolzargs contains core filtering and ordering logic for web applications. The main feature are:

- Filtering and

- ordering for SQLAlchemy models.

## Installation

```bash
pip install wtoolzargs
```

## Getting Up and Running

```bash
nox -l
```

## Examples

```python
import wtoolzargs

# sqlalchemy model
class Hacker(Base):
    __tablename__ = "hacker"
    id = Column(Integer, primary_key=True)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    e = Column(String)

f = wtoolzargs.filter_(Hacker, "a eq 'a' and b eq 'b'")
res = Hacker.query.filter(f).all()

o = wtoolzargs.order(Hacker, "a asc, b desc")
res = Hacker.query.filter(f).order_by(*o).all()    
```

## API

FIXME

## See Also

FIXME
