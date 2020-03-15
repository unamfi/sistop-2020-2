Future<int> doSomeLongTask() async {
  await Future.delayed(const Duration(seconds: 5));
  return 0;
}

main () async {
  int result = await doSomeLongTask();
  print(result);
}
