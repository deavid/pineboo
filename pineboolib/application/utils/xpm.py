import os
import os.path

from pineboolib.core.settings import config


def cacheXPM(value: str) -> str:
    if not value:
        raise ValueError("Expected a value")
    xpm_name = value[: value.find("[]")]
    xpm_name = xpm_name[xpm_name.rfind(" ") + 1 :]
    from pineboolib.application import project

    if project.conn is None:
        raise Exception("Project is not connected yet")

    cache_dir = "%s/cache/%s/cacheXPM" % (project.tmpdir, project.conn.DBName())
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    if value.find("cacheXPM") > -1:
        file_name = value
    else:
        file_name = "%s/%s.xpm" % (cache_dir, xpm_name)

    if not os.path.exists(file_name) or config.value(
        "ebcomportamiento/no_img_cached", False
    ):
        f = open(file_name, "w")
        f.write(value)
        f.close()

    return file_name
