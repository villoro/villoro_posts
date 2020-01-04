import luigi

from datetime import date, datetime


class RegisterTask(luigi.Task):

    mdate = luigi.DateParameter(default=date.today())

    def run(self):
        from register import main

        main(self.mdate.strftime("%Y_%m_%d"))

    def output(self):
        return luigi.LocalTarget(self.mdate.strftime("output/%Y_%m_%d.txt"))


class ReportTask(luigi.Task):

    mdate = luigi.DateParameter(default=date.today())

    def run(self):
        from report import main

        main(self.mdate.strftime("%Y_%m_%d"))

    def output(self):
        return luigi.LocalTarget(self.mdate.strftime("output/%Y_%m_%d.html"))


class DoAllTask(luigi.WrapperTask):

    mdate = luigi.DateParameter(default=date.today())

    def requires(self):
        return RegisterTask(self.mdate), ReportTask(self.mdate)


if __name__ == "__main__":
    luigi.build([DoAllTask()])
