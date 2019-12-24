#ifndef __PRINTF_S_HPP_INCLUDED__
#define __PRINTF_S_HPP_INCLUDED__

/*
Средствами Си есть идея сделать wrapper(define) за счет которого сейвить rbp и потом чекать offset
*/

#include <string_view>
#include <stdexcept>

namespace detail
{
    inline constexpr char FMT_SPEC = '%';

    constexpr std::size_t count_args(const std::string_view str)
    {
        std::size_t count{};
        auto length = str.length();
        for(std::size_t i{}; i < length; ++i)
            if(str[i] == FMT_SPEC && ++i != length && str[i] != FMT_SPEC)
                count++;
        
        return count;
    }
} // namespace detail

template<typename _Arg, typename... _Args>
void printf_s(std::string_view format, _Arg&& arg, _Args&&... args)
{
    if(detail::count_args(format) != sizeof...(args) + 1)
        throw std::invalid_argument("Number of args does not match the given format");

    // TODO: Call printf for proper args. Check conformity between % and arg
}

#endif /* !__PRINTF_S_HPP_INCLUDED__ */