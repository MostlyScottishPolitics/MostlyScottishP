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
    # spsession = models.ManyToManyField(SPsession)
    foreignid = models.PositiveIntegerField(max_length=8, unique=True)
    constituency = models.ForeignKey(Constituency)
    party = models.ForeignKey(Party)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    job = models.CharField(max_length=128)
    img = models.CharField(max_length=256)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)


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

    parent = models.ForeignKey('self', default=0,  null=True)
    date = models.DateField(null=True)
    number = models.IntegerField(null=True)
    link = models.URLField(max_length=128, null=True)
    question = models.TextField(null=True)
    motionid = models.CharField(max_length=12)
    motiontext = models.TextField()
    topic = models.CharField(max_length=30, null=True)
    votes = models.ManyToManyField(MSP, through='Vote', null=True)
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

    def __unicode__(self):
        return self.vote