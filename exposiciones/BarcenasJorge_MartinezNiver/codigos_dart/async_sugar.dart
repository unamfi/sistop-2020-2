Stream<int> countForOneMinute() async* {
  for(int i=1; i <= 15; i++) {
    await Future.delayed(const Duration(seconds: 3));
    yield i;
  }
}

main() async {
  await for (int i in countForOneMinute()) {
	print(i);
  }
}
