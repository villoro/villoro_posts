import luigi

from luigi_default import StandardTask


class RegisterTask(StandardTask):
    module = "register"


class ReportTask(StandardTask):
    module = "report"


class DoAllTask(StandardTask):
    def run_std(self):
        with open(self.mdate.strftime("output/%Y_%m_%d.info"), "w") as stream:
            stream.write("Done")

    def requires(self):
        return RegisterTask(self.mdate), ReportTask(self.mdate)


if __name__ == "__main__":
    luigi.build([DoAllTask()])
