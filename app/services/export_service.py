from fastapi.responses import Response, PlainTextResponse, JSONResponse
import dicttoxml

def export_data(data, formato, download=False):
    
    headers = {}
    if download:
        ext = formato if formato in ["json", "xml", "txt"] else "json"
        headers["Content-Disposition"] = f'attachment; filename="eventos.{ext}"'

    if formato == "json":
        return JSONResponse(content=data, headers=headers if download else None)

    if formato == "xml":
        # attr_type=False elimina los type="str" molestos y hace un XML más limpio.
        xml = dicttoxml.dicttoxml(data, custom_root='eventos', attr_type=False)

        return Response(
            content=xml,
            media_type="application/xml",
            headers=headers if download else None
        )

    if formato == "txt":
        texto = ""
        for d in data:
            texto += str(d) + "\n"

        return PlainTextResponse(
            content=texto, 
            headers=headers if download else None
        )