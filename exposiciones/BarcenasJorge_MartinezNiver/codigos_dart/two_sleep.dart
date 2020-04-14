Stream<int> count() async* {
  for(int i=1; i <= 15; i++) {
    await sleep1();
    yield i;
  }
  for(int i=1; i <= 10; i++) {
    await sleep2();
    yield i;
  }
}

Future sleep1() {
  return new Future.delayed(const Duration(seconds: 1), () => "1");
}

Future sleep2() {
  return new Future.delayed(const Duration(seconds: 2), () => "2");
}

main() async {
  await for (int i in count()) {
	print(i);
  }
}