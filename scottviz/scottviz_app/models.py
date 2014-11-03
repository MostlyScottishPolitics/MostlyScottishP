from django.db import models


class Party(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Constituency(models.Model):
    # msps = models.ManyToManyField(MSP)
    # Type = models.BooleanField()
    parent = models.ForeignKey('self', default=0, null=True)
    name = models.CharField(max_length=128, unique=True)
    # regionname = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class MSP(models.Model):
    # constituency = models.ManyToManyField(Constituency)
    # votes = models.ForeignKey(Vote,unique=True)
    # divisions = models.ForeignKey(Division, unique=True)
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
        return self.name


class Division(models.Model):
    CARRIED = 1
    DEFEATED = 2

    RESULTS = (
        (CARRIED, 'Carried'),
        (DEFEATED, 'Defeated')
    )

    # votes = models.ForeignKey(Vote,unique=True)
    # msp = models.ForeignKey(MSP, unique=True)
    # agreement = models.BooleanField()


    parent = models.ForeignKey('self', default=0)
    date = models.DateField()
    number = models.IntegerField()
    link = models.URLField(max_length=128)
    question = models.TextField()
    motionid = models.CharField(max_length=12)
    motiontext = models.TextField()
    topic = models.CharField(max_length=30)
    votes = models.ManyToManyField(MSP, through='Vote')
    result = models.CharField(max_length=1, choices=RESULTS)

    def __unicode__(self):
        return self.name


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

    msp = models.ForeignKey(MSP, unique=True)
    divisions = models.ForeignKey(Division, unique=True)
    vote = models.CharField(max_length=1, choices=VOTES)

    def __unicode__(self):
        return self.name