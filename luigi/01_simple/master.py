import luigi

from datetime import date, datetime


class RegisterTask(luigi.Task):

    mdate = luigi.DateParameter(default=date.today())

    def run(self):
        from register import do

        do(mdate.strftime("%Y_%m_%d"))

    def output(self):
        return luigi.LocalTarget(self.mdate.strftime("output/%Y_%m_%d.txt"))


class ReportTask(luigi.Task):

    mdate = luigi.DateParameter(default=date.today())

    def run(self):
        from report import do

        do(mdate.strftime("%Y_%m_%d"))

    def output(self):
        return luigi.LocalTarget(self.mdate.strftime("output/%Y_%m_%d.html"))


class DoAllTask(luigi.Task):

    mdate = luigi.DateParameter(default=date.today())

    def get_uri(self):
        return self.mdate.strftime("output/%Y_%m_%d.info")

    def run(self):
        with open(self.get_uri(), "w") as stream:
            stream.write("Done")

    def output(self):
        return luigi.LocalTarget(self.get_uri())

    def requires(self):
        return RegisterTask(self.mdate), ReportTask(self.mdate)


if __name__ == "__main__":
    luigi.build([DoAllTask()])
