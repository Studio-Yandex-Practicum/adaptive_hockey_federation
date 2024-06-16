from main.admin.admin import (CityAdmin, DiagnosisAdmin, DisciplineLevelAdmin,
                              DisciplineNameAdmin, NosologyAdmin, PlayerAdmin,
                              StaffMemberAdmin, TeamAdmin, admin)
from main.models import (City, Diagnosis, DisciplineLevel, DisciplineName,
                         Nosology, Player, StaffMember, Team)

admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(DisciplineLevel, DisciplineLevelAdmin)
admin.site.register(DisciplineName, DisciplineNameAdmin)
admin.site.register(Nosology, NosologyAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(City, CityAdmin)
