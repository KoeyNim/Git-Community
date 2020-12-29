import re
from django.core.exceptions import ValidationError

def SignupValidate(value):
    # 최솟값
    if len(value) < 3:
        raise ValidationError(
            ('글자 수를 맞추어 주세요.(3~17)'),
            params={'value': value},
        )
    # 한글, 영문, 숫자 (특수문자, 공백 미포함)
    elif value.isalnum() == False:
        raise ValidationError(
            ('특수문자 및 공백은 사용할 수 없습니다.'),
            params={'value': value},
        )
    # 영문 대소문자, 숫자 search = 전체 검색
    elif re.search('[ㄱ-ㅣ가-힣]+', value) is not None:
        raise ValidationError(
            ('아이디는 영문, 숫자만 가능합니다.'),
            params={'value': value},
        )
    # 첫 글자만 탐색 match = 처음부터 검색
    elif re.match('[a-zA-Z]', value) is None:
        raise ValidationError(
            ('첫 글자는 영문만 가능합니다.'),
            params={'value': value},
        )
    # 하나 이상의 숫자를 포함
    elif re.search('[0-9]+', value) is None:
        raise ValidationError(
            ('최소 하나이상의 숫자를 입력해야 합니다.'),
            params={'value': value},
        )