from django.db import models


class Party(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Constituency(models.Model):
    parent = models.ForeignKey('self', default=0, null=True)
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class MSP(models.Model):

    MEMBER = 1
    RESIGNED = 2
    DECEASED = 3

    SITUATIONS = (
        (MEMBER, 'Member'),
        (RESIGNED, 'Resigned'),
        (DECEASED, 'Deceased')
    )

    # spsession = models.ManyToManyField(SPsession)
    foreignid = models.PositiveIntegerField(max_length=8, unique=True)
    member_startdate = models.DateField(null=True)
    member_enddate = models.DateField(null=True)
    constituency = models.ForeignKey(Constituency)
    party = models.ForeignKey(Party)
    party_startdate = models.DateField(null=True)
    party_enddate = models.DateField(null=True)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    img = models.CharField(max_length=256)
    presence=models.DecimalField(max_digits=5, decimal_places=2, null=True)
    rebellions=models.DecimalField(max_digits=5, decimal_places=2, null=True)
    status = models.CharField(max_length=1, choices=SITUATIONS)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

class Job(models.Model):
    job_foreignid = models.PositiveIntegerField(max_length=8, unique=True)
    name = models.CharField(max_length=128)
    msp = models.ForeignKey(MSP)
    job_startdate = models.DateField()
    job_enddate = models.DateField()

    def __unicode__(self):
        return u'%s: %s - %s' (self.name, self.job_startdate, self.job_enddate)

class SPsession(models.Model):
    msps = models.ManyToManyField(MSP)
    session = models.IntegerField()
    startdate = models.DateField()
    enddate = models.DateField()

    def __unicode__(self):
        return self.session


class Division(models.Model):
    CARRIED = 1
    DEFEATED = 2

    RESULTS = (
        (CARRIED, 'Carried'),
        (DEFEATED, 'Defeated')
    )
    # number = models.IntegerField(null=True)

    parent = models.ForeignKey('self', default=0, null=True)
    date = models.DateField(null=True)
    proposer = models.ForeignKey(MSP, related_name='msp_proposer', null=True)
    link = models.URLField(max_length=128, null=True)
    question = models.TextField(null=True)
    motionid = models.CharField(max_length=20)
    motiontext = models.TextField()
    topic = models.CharField(max_length=30, null=True)
    votes = models.ManyToManyField(MSP, through='Vote', null=True)
    turnout=models.DecimalField(max_digits=5, decimal_places=2, null=True)
    rebels=models.IntegerField(null=True)
    result = models.CharField(max_length=1, choices=RESULTS)

    def __unicode__(self):
        return self.motionid


class Vote(models.Model):
    YES = 1
    NO = 2
    ABSTAIN = 3
    ABSENT = 4
    VOTES = (
        (YES, 'Yes'),
        (NO, 'No'),
        (ABSTAIN, 'Abstain'),
        (ABSENT, 'Absent')
    )

    msp = models.ForeignKey(MSP)
    division = models.ForeignKey(Division)
    vote = models.CharField(max_length=1, choices=VOTES, null=True)
    rebellious = models.BooleanField()
    party_vote = models.CharField(max_length=1, choices=VOTES, null=True)

    def __unicode__(self):
        return self.vote