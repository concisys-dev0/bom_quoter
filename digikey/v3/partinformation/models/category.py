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


class Category(object):
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
        'category_id': 'int',
        'parent_id': 'int',
        'name': 'str',
        'product_count': 'int',
        'children': 'list[Category]'
    }

    attribute_map = {
        'category_id': 'CategoryId',
        'parent_id': 'ParentId',
        'name': 'Name',
        'product_count': 'ProductCount',
        'children': 'Children'
    }

    def __init__(self, category_id=None, parent_id=None, name=None, product_count=None, children=None, _configuration=None):  # noqa: E501
        """Category - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._category_id = None
        self._parent_id = None
        self._name = None
        self._product_count = None
        self._children = None
        self.discriminator = None

        if category_id is not None:
            self.category_id = category_id
        if parent_id is not None:
            self.parent_id = parent_id
        if name is not None:
            self.name = name
        if product_count is not None:
            self.product_count = product_count
        if children is not None:
            self.children = children

    @property
    def category_id(self):
        """Gets the category_id of this Category.  # noqa: E501

        Gets or Sets CategoryId  # noqa: E501

        :return: The category_id of this Category.  # noqa: E501
        :rtype: int
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """Sets the category_id of this Category.

        Gets or Sets CategoryId  # noqa: E501

        :param category_id: The category_id of this Category.  # noqa: E501
        :type: int
        """

        self._category_id = category_id

    @property
    def parent_id(self):
        """Gets the parent_id of this Category.  # noqa: E501

        The Id of the Partent Category if the given category is a child of another category  # noqa: E501

        :return: The parent_id of this Category.  # noqa: E501
        :rtype: int
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this Category.

        The Id of the Partent Category if the given category is a child of another category  # noqa: E501

        :param parent_id: The parent_id of this Category.  # noqa: E501
        :type: int
        """

        self._parent_id = parent_id

    @property
    def name(self):
        """Gets the name of this Category.  # noqa: E501

        Gets or Sets Name  # noqa: E501

        :return: The name of this Category.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Category.

        Gets or Sets Name  # noqa: E501

        :param name: The name of this Category.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def product_count(self):
        """Gets the product_count of this Category.  # noqa: E501

        Gets or Sets ProductCount  # noqa: E501

        :return: The product_count of this Category.  # noqa: E501
        :rtype: int
        """
        return self._product_count

    @product_count.setter
    def product_count(self, product_count):
        """Sets the product_count of this Category.

        Gets or Sets ProductCount  # noqa: E501

        :param product_count: The product_count of this Category.  # noqa: E501
        :type: int
        """

        self._product_count = product_count

    @property
    def children(self):
        """Gets the children of this Category.  # noqa: E501

        List of Child Categories  # noqa: E501

        :return: The children of this Category.  # noqa: E501
        :rtype: list[Category]
        """
        return self._children

    @children.setter
    def children(self, children):
        """Sets the children of this Category.

        List of Child Categories  # noqa: E501

        :param children: The children of this Category.  # noqa: E501
        :type: list[Category]
        """

        self._children = children

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
        if issubclass(Category, dict):
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
        if not isinstance(other, Category):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Category):
            return True

        return self.to_dict() != other.to_dict()
