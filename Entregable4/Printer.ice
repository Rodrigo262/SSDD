module Example {
  interface Printer {
    void write(string message);
  };
  interface Statistics {
    void notify(string printerId);
  };
};
