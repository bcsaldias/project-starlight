from django.db import models

from user.models import Expert

CHOICES = [ ('CEP','Cepheid'),
            ('RRLYR','RR Lyrae'), 
            ('LPV','Long-period variable'), 
            ('EB','Eclipsing Binary')]

class CatalinaObject(models.Model):

    catalina_id = models.CharField(max_length=120, primary_key=True)
    hidden_id = models.CharField(max_length=120, unique=True)
    RA = models.CharField(max_length=50, null=True)
    Dec = models.CharField(max_length=50, null=True)
    V = models.CharField(max_length=50, null=True)
    Period = models.CharField(max_length=50, null=True)
    Amplitude = models.FloatField(blank=True, null=True)

    folded_image = models.ImageField(default = 'media/None/no-img.png')
    original_image = models.ImageField(default = 'media/None/no-img.png')

    Var_Type = models.CharField(max_length=50, null=True, choices=CHOICES)

    _training = models.BooleanField(default=False)
    _validation = models.BooleanField(default=False)
    _abc = models.BooleanField(default=False)

    def __str__(self):
        return self.catalina_id

class Vote(models.Model):

    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    object = models.ForeignKey(CatalinaObject, on_delete=models.CASCADE, related_name="votes")
    question = models.CharField(max_length=15, null=True)
    value = models.BooleanField()
    milliseconds = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['expert','object','question']


    def __str__(self):
        return "{} voted {} for: is this a {}?".format(self.expert, self.value, self.question)

class PendingQuestion(models.Model):

    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    object = models.ForeignKey(CatalinaObject, on_delete=models.CASCADE)
    question = models.CharField(max_length=25, null=True, choices=CHOICES)

    class Meta:
        unique_together = ['expert','object','question']


    #def __str__(self):
    #    return "{} is asked: is {} a {}?".format(self.expert, self.object, self.question)

class FullVote(models.Model):

    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    object = models.ForeignKey(CatalinaObject, on_delete=models.CASCADE, related_name="full_votes")
    value = models.CharField(max_length=8, null=True, choices=CHOICES)
    milliseconds = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['expert','object']

    def __str__(self):
        return "{} voted {}".format(self.expert, self.value)

class FullPendingQuestion(models.Model):

    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    object = models.ForeignKey(CatalinaObject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['expert','object']

    #def __str__(self):
    #    return "{} is asked for {}?".format(self.expert, self.object)


class MACHOObject(models.Model):

    macho_id = models.CharField(max_length=120, primary_key=True)
    Amplitude = models.FloatField(blank=True, null=True)
    AndersonDarling = models.FloatField(blank=True, null=True)
    Autocor_length = models.FloatField(blank=True, null=True)
    Beyond1Std = models.FloatField(blank=True, null=True)
    CAR_mean = models.FloatField(blank=True, null=True)
    CAR_sigma = models.FloatField(blank=True, null=True)
    CAR_tau = models.FloatField(blank=True, null=True)
    Color = models.FloatField(blank=True, null=True)
    Con = models.FloatField(blank=True, null=True)
    Eta_color = models.FloatField(blank=True, null=True)
    Eta_e = models.FloatField(blank=True, null=True)
    FluxPercentileRatioMid20 = models.FloatField(blank=True, null=True)
    FluxPercentileRatioMid35 = models.FloatField(blank=True, null=True)
    FluxPercentileRatioMid50 = models.FloatField(blank=True, null=True)
    FluxPercentileRatioMid65 = models.FloatField(blank=True, null=True)
    FluxPercentileRatioMid80 = models.FloatField(blank=True, null=True)
    Freq1_harmonics_amplitude_0 = models.FloatField(blank=True, null=True)
    Freq1_harmonics_amplitude_1 = models.FloatField(blank=True, null=True)
    Freq1_harmonics_amplitude_2 = models.FloatField(blank=True, null=True)
    Freq1_harmonics_amplitude_3 = models.FloatField(blank=True, null=True)
    Freq1_harmonics_rel_phase_0 = models.FloatField(blank=True, null=True)
    Freq1_harmonics_rel_phase_1 = models.FloatField(blank=True, null=True)
    Freq1_harmonics_rel_phase_2 = models.FloatField(blank=True, null=True)
    Freq1_harmonics_rel_phase_3 = models.FloatField(blank=True, null=True)
    Freq2_harmonics_amplitude_0 = models.FloatField(blank=True, null=True)
    Freq2_harmonics_amplitude_1 = models.FloatField(blank=True, null=True)
    Freq2_harmonics_amplitude_2 = models.FloatField(blank=True, null=True)
    Freq2_harmonics_amplitude_3 = models.FloatField(blank=True, null=True)
    Freq2_harmonics_rel_phase_0 = models.FloatField(blank=True, null=True)
    Freq2_harmonics_rel_phase_1 = models.FloatField(blank=True, null=True)
    Freq2_harmonics_rel_phase_2 = models.FloatField(blank=True, null=True)
    Freq2_harmonics_rel_phase_3 = models.FloatField(blank=True, null=True)
    Freq3_harmonics_amplitude_0 = models.FloatField(blank=True, null=True)
    Freq3_harmonics_amplitude_1 = models.FloatField(blank=True, null=True)
    Freq3_harmonics_amplitude_2 = models.FloatField(blank=True, null=True)
    Freq3_harmonics_amplitude_3 = models.FloatField(blank=True, null=True)
    Freq3_harmonics_rel_phase_0 = models.FloatField(blank=True, null=True)
    Freq3_harmonics_rel_phase_1 = models.FloatField(blank=True, null=True)
    Freq3_harmonics_rel_phase_2 = models.FloatField(blank=True, null=True)
    Freq3_harmonics_rel_phase_3 = models.FloatField(blank=True, null=True)
    LinearTrend = models.FloatField(blank=True, null=True)
    MaxSlope = models.FloatField(blank=True, null=True)
    Mean = models.FloatField(blank=True, null=True)
    Meanvariance = models.FloatField(blank=True, null=True)
    MedianAbsDev = models.FloatField(blank=True, null=True)
    MedianBRP = models.FloatField(blank=True, null=True)
    PairSlopeTrend = models.FloatField(blank=True, null=True)
    PercentAmplitude = models.FloatField(blank=True, null=True)
    PercentDifferenceFluxPercentile = models.FloatField(blank=True, null=True)
    PeriodLS = models.FloatField(blank=True, null=True)
    Period_fit = models.FloatField(blank=True, null=True)
    Psi_CS = models.FloatField(blank=True, null=True)
    Psi_eta = models.FloatField(blank=True, null=True)
    Q31 = models.FloatField(blank=True, null=True)
    Q31_color = models.FloatField(blank=True, null=True)
    Rcs = models.FloatField(blank=True, null=True)
    Skew = models.FloatField(blank=True, null=True)
    SlottedA_length = models.FloatField(blank=True, null=True)
    SmallKurtosis = models.FloatField(blank=True, null=True)
    Std = models.FloatField(blank=True, null=True)
    StetsonJ = models.FloatField(blank=True, null=True)
    StetsonK = models.FloatField(blank=True, null=True)
    StetsonK_AC = models.FloatField(blank=True, null=True)
    StetsonL = models.FloatField(blank=True, null=True)
    label = models.CharField(max_length=15, null=True)

    folded_image = models.ImageField(default = 'media/None/no-img.png')
    original_image = models.ImageField(default = 'media/None/no-img.png')

    def __str__(self):
        return self.macho_id