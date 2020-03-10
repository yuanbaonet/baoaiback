"""status

Custom Response Status
定制响应状态

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

class Status():
    class SUCCESS:
        status = 200000
        message = "Success"

    class ERROR:
        status = 200400
        message = "Error"

    class TOKEN_SUCCESS:
        status = 200001
        message = "Token Success"

    class PARAMETER_ERROR:
        status = 400422
        message = "Parameter Error"

    class FORBIDDEN:
        status = 400403
        message = "Forbidden!"

    class FILE_NOT_FOUND:
        status = 400404
        message = "Forbidden!"

    class INTERNAL_ERROR:
        status = 500000
        message = "Internal Error"

    class TOKEN_ERROR:
        status = 500001
        message = "Token Error"

    class TOKEN_SIGNATURE_EXPIRED:
        status = 500002
        message = "Token Signature Expired"

    class TOKEN_BADSIGNATURE:
        status = 500003
        message = "Token BadSignature"

    class TOKEN_TAMPERED:
        status = 500004
        message = "Token Tampered"

    class TOKEN_UNKNOWN_REASON:
        status = 500005
        message = "Error Token With Unknown Reason"

    class TOKEN_ILLEGAL:
        status = 500005
        message = "Illegal Payload Inside"
