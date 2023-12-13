ALBUM_MENUS_QUERY = """
*[_type == 'albumMenu' && isActive == true {NAME_FILTER}] {{
    _id,
    menuName,
    flyer->{{
      _id,
      title,
      image {{asset->{{url}}}}
    }},
    albumSections[]->{{
      sectionName,
      albums[]->{{
        albumName,
        albumLink,
        albumCover{{asset->{{url}}}},
        genres[]->{{
          genreName
        }}
      }}
    }}
}}
"""
