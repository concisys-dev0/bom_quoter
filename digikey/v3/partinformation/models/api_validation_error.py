# coding: utf-8

"""
    PartSearch Api

    Search for products and retrieve details and pricing.  # noqa: E501

    OpenAPI spec version: Ps2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from partinformation.configuration import Configuration


class ApiValidationError(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'field': 'str',
        'message': 'str'
    }

    attribute_map = {
        'field': 'Field',
        'message': 'Message'
    }

    def __init__(self, field=None, message=None, _configuration=None):  # noqa: E501
        """ApiValidationError - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._field = None
        self._message = None
        self.discriminator = None

        if field is not None:
            self.field = field
        if message is not None:
            self.message = message

    @property
    def field(self):
        """Gets the field of this ApiValidationError.  # noqa: E501

        The field that generated the error.  # noqa: E501

        :return: The field of this ApiValidationError.  # noqa: E501
        :rtype: str
        """
        return self._field

    @field.setter
    def field(self, field):
        """Sets the field of this ApiValidationError.

        The field that generated the error.  # noqa: E501

        :param field: The field of this ApiValidationError.  # noqa: E501
        :type: str
        """

        self._field = field

    @property
    def message(self):
        """Gets the message of this ApiValidationError.  # noqa: E501

        The error message that was generated. This often explains how to fix your API input to be valid.  # noqa: E501

        :return: The message of this ApiValidationError.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ApiValidationError.

        The error message that was generated. This often explains how to fix your API input to be valid.  # noqa: E501

        :param message: The message of this ApiValidationError.  # noqa: E501
        :type: str
        """

        self._message = message

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ApiValidationError, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiValidationError):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApiValidationError):
            return True

        return self.to_dict() != other.to_dict()
