import requests
import json
from optparse import OptionParser


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {"content-type": "application/json"}
    parser = OptionParser()
    parser.add_option("-m", "--method", dest="method", help="metodo a llamar", metavar="METHOD")
    parser.add_option("-p", "--params", dest="params", help="parametros pasados", metavar="PARAMS")

    (options, args) = parser.parse_args()
    # Example echo method
    _method = "None"
    if options.method is not None:
        _method = options.method
    _params = []
    if options.params is not None:
        if options.params.find(":") > -1:
            for op in options.params.split(":"):
                _params.append(op)

        else:
            _params.append(options.params)

    payload = {"method": _method, "params": _params, "jsonrpc": "2.0", "id": 0}
    print("Enviando:", payload)
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()

    if "result" in response.keys():
        print("Respuesta:", response["result"])
    else:
        print("Error code: %s - %s" % (response["error"]["code"], response["error"]["message"]))
    # assert response["result"] == "echome!"
    # assert response["jsonrpc"]
    # assert response["id"] == 0


if __name__ == "__main__":
    main()
