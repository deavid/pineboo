import os
import os.path

from pineboolib.core.settings import config


def cacheXPM(value):
    file_name = None
    if value:
        xpm_name = value[: value.find("[]")]
        xpm_name = xpm_name[xpm_name.rfind(" ") + 1 :]
        from pineboolib.pncontrolsfactory import aqApp

        cache_dir = "%s/cache/%s/cacheXPM" % (aqApp.tmp_dir(), aqApp.db().DBName())
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        if value.find("cacheXPM") > -1:
            file_name = value
        else:
            file_name = "%s/%s.xpm" % (cache_dir, xpm_name)

        if not os.path.exists(file_name) or config.value("ebcomportamiento/no_img_cached", False):
            f = open(file_name, "w")
            f.write(value)
            f.close()

    return file_name
