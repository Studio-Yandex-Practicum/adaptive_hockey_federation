from main.admin.admin import (
    CityAdmin,
    DiagnosisAdmin,
    DisciplineAdmin,
    DisciplineLevelAdmin,
    DisciplineNameAdmin,
    DocumentAdmin,
    NosologyAdmin,
    PlayerAdmin,
    StaffMemberAdmin,
    StaffTeamMemberAdmin,
    TeamAdmin,
    admin,
)
from main.models import (
    City,
    Diagnosis,
    Discipline,
    DisciplineLevel,
    DisciplineName,
    Document,
    Nosology,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)

admin.site.register(City, CityAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(DisciplineLevel, DisciplineLevelAdmin)
admin.site.register(DisciplineName, DisciplineNameAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Nosology, NosologyAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(StaffTeamMember, StaffTeamMemberAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(Team, TeamAdmin)
