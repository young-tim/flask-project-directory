# -*-coding:utf-8-*-
from apps.configs.config import PER_PAGE


def datas_paging(pre=PER_PAGE, current=1, total=0, datas=[]):
    '''
    分页函数
    :param pre: 每页数量
    :param current: 当前页
    :param total: 数据总条数
    :param datas: 列表数据
    :return: {
        items: 列表数据集，
        total: 数据总条数
        page_size: 每页数据条数
        page_count: 分页总数，
        current_page: 当前页，
    }
    '''
    if total % pre == 0:
        page_count = total // pre
    else:
        page_count = total // pre + 1

    if current > 1:
        prev_num = current - 1
        has_prev = True
    else:
        prev_num = None
        has_prev = False

    if current < page_count:
        next_num = current + 1
        has_next = True
    else:
        next_num = None
        has_next = False

    obj = {
        "page_size": len(datas),  # 当前页内容数量
        "page": current,  # 页数
        "prev_num": prev_num,  # 上一页数值
        "next_num": next_num,  # 下一页数值
        "has_next": has_next,  # 是否有下一页
        "has_prev": has_prev,  # 是否有上一页
        "per_page": pre,  # 每页内容数量
        "pages": page_count,  # 总页数
        "total": total,  # 总数据数
        "items": datas,  # 数据集
    }

    return obj


def paginate_to_obj(paginate, datas=[]):
    """
    将ORM的paginate对象转化为dict格式
    :param paginate: ORM的paginate对象
    :param datas: 数据集，如为空，将从paginate对象中循环取出
    :return: dict data
    """
    if paginate:
        obj = {"page_size": len(paginate.items),  # 当前页内容数量
               "page": paginate.page,  # 页数
               "prev_num": paginate.prev_num,  # 上一页数值
               "next_num": paginate.next_num,  # 下一页数值
               "has_next": paginate.has_next,  # 是否有下一页
               "has_prev": paginate.has_prev,  # 是否有上一页
               "per_page": paginate.per_page,  # 每页内容数量
               "pages": paginate.pages,  # 总页数
               "total": paginate.total  # 总数据数
               }
        if datas == []:
            # 循环数据
            list = []
            for v in paginate.items:
                list.append(v.toDict())

            obj["items"] = list
        else:
            obj["items"] = datas

        return obj
    else:
        # 无paginate参数，直接返回空对象
        return {}
